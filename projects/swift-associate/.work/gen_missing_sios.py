#!/usr/bin/env python3
"""
gen_missing_sios_llm.py
Gọi LLM để sinh SIOs semantic cho các CIO thiếu (< 2 SIOs).
Chỉ xử lý CIOs thiếu, không ảnh hưởng các SIOs đã có.
"""
import json, os, re, sys
from pathlib import Path

try:
    from openai import OpenAI
    import httpx
except ImportError:
    print("[ERROR] pip install openai httpx", file=sys.stderr)
    sys.exit(1)

BASE = Path("projects/swift-associate")
HLO  = BASE / ".work/hlo"
OUT  = BASE / "output"

CIOS_PATH = HLO / "cios.json"
SIOS_PATH = HLO / "sios.json"
TSV_PATH  = OUT / "learning-objectives.tsv"

with open(CIOS_PATH) as f: cios = json.load(f)
with open(SIOS_PATH) as f: existing_sios = json.load(f)

cio_map = {c["code"]: c for c in cios}

# ─── Build CIO → SIO count ───────────────────────────────────────────────────
cio_sio_count: dict[str,int] = {c["code"]: 0 for c in cios}
for s in existing_sios:
    p = s.get("parent_cio_code","")
    if p in cio_sio_count:
        cio_sio_count[p] += 1

lacking_codes = [code for code, cnt in cio_sio_count.items() if cnt < 2]
lacking_cios  = [cio_map[c] for c in lacking_codes if c in cio_map]
print(f"CIOs cần sinh SIOs: {len(lacking_cios)}")

# ─── LLM setup ───────────────────────────────────────────────────────────────
api_key  = os.environ.get("OPENAI_API_KEY","")
base_url = os.environ.get("OPENAI_BASE_URL")
if not api_key:
    print("[ERROR] OPENAI_API_KEY chưa set", file=sys.stderr)
    sys.exit(1)

# Use explicit http_client to bypass httpx proxy URL parsing issue with Ollama
http_client = httpx.Client(transport=httpx.HTTPTransport())
client = OpenAI(api_key=api_key, base_url=base_url or None, http_client=http_client)
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4.1")

SYSTEM = """Bạn là Chuyên gia Thiết kế Curriculum viết Specific Implementation Objectives (SIO) cho Swift.

SIO = Tầng Implementational: kỹ năng CỤ THỂ bằng Swift/SwiftUI/UIKit.

Nguyên tắc:
1. SIO BẮT BUỘC nhắc tên công nghệ "Swift" trong name và description
2. NÊN nhắc tên API, keyword cụ thể của Swift/SwiftUI/UIKit (ví dụ: @State, withAnimation, .frame(), Array subscript...)
3. Mỗi CIO cần ĐÚNG 2 SIO con — 2 scenario/cách thể hiện khác nhau (không chỉ repeat)
4. Description bắt đầu "Người học có khả năng ..." (tiếng Việt, 2–3 câu cụ thể có ví dụ code)
5. bloom_level = cùng bloom của CIO hoặc Apply (SIOs thiên về thực hành)
6. knowledge_dimension = PROCEDURAL (SIOs là kỹ năng thực hành)
7. Code SIO: SIO-SWIFT-<SEMANTIC_SLUG> (UPPER_SNAKE_CASE, mô tả hành động cụ thể)

Trả về JSON hợp lệ theo schema cho trước.
"""

# ─── CIO all codes (for reference) ───────────────────────────────────────────
cio_summary = "\n".join(f"  {c['code']}" for c in cios)

# ─── Batch processing ─────────────────────────────────────────────────────────
BATCH_SIZE = 3  # small batch = less JSON errors from LLM
all_new_sios = []
existing_sio_codes = {s["code"] for s in existing_sios}

for i in range(0, len(lacking_cios), BATCH_SIZE):
    batch = lacking_cios[i : i + BATCH_SIZE]
    batch_text = "\n\n".join(
        f"CIO: {c['code']}\n"
        f"  Name: {c['name']}\n"
        f"  Bloom: {c['bloom_level']} | Dim: {c['knowledge_dimension']}\n"
        f"  Mô tả: {c.get('description_vi','')[:200]}"
        for c in batch
    )

    user_prompt = (
        f"Danh sách tất cả CIO (để reference parent_cio_code):\n{cio_summary}\n\n"
        f"Sinh 2 SIOs cho MỖI CIO dưới đây (tổng {len(batch)*2} SIOs):\n\n{batch_text}\n\n"
        "Trả về JSON:\n"
        '{ "sios": [ { "code": "SIO-SWIFT-...", "name": "...", '
        '"description_vi": "Người học có khả năng ...", '
        '"bloom_level": "...", "knowledge_dimension": "PROCEDURAL", '
        '"parent_cio_code": "CIO-..." } ] }'
    )

    print(f"\n[Batch {i//BATCH_SIZE + 1}] {len(batch)} CIOs → ~{len(batch)*2} SIOs ...")
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user",   "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
        )
        raw = resp.choices[0].message.content

        # Robust JSON parsing
        def try_parse_json(text: str) -> dict:
            # Strip markdown code fences
            text = text.strip()
            if text.startswith("```"):
                text = re.sub(r"```(?:json)?\n?", "", text).strip()
            # Try direct parse
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                pass
            # Try to extract JSON object with regex
            m = re.search(r'\{[\s\S]*\}', text)
            if m:
                try:
                    return json.loads(m.group())
                except json.JSONDecodeError:
                    pass
            # Last resort: fix escaped backslashes
            try:
                return json.loads(text.replace("\\", "\\\\"))
            except:
                raise ValueError(f"Cannot parse JSON from LLM response: {text[:200]}")

        data = try_parse_json(raw)
        batch_sios = data.get("sios", [])

        # Validate: must reference a real CIO and have unique code
        batch_cio_codes = {c["code"] for c in batch}
        valid = []
        for s in batch_sios:
            if s.get("parent_cio_code","") not in cio_map:
                print(f"  [SKIP] bad parent: {s.get('parent_cio_code')}")
                continue
            code = s.get("code","")
            if code in existing_sio_codes or code in {x["code"] for x in all_new_sios}:
                code = code + "_2"
                s["code"] = code
            valid.append(s)
            print(f"  + {s['code']} → {s['parent_cio_code']}")

        all_new_sios.extend(valid)
        print(f"  Batch done: +{len(valid)} SIOs")

    except Exception as e:
        print(f"  [ERROR] {e}", file=sys.stderr)
        import traceback; traceback.print_exc(file=sys.stderr)

# ─── Write sios.json ──────────────────────────────────────────────────────────
merged_sios = existing_sios + all_new_sios
with open(SIOS_PATH, "w", encoding="utf-8") as f:
    json.dump(merged_sios, f, ensure_ascii=False, indent=2)
print(f"\n[OK] sios.json: {len(existing_sios)} + {len(all_new_sios)} = {len(merged_sios)} total SIOs")

# ─── Append to TSV ────────────────────────────────────────────────────────────
with open(TSV_PATH, encoding="utf-8") as f:
    tsv_lines = f.readlines()
tsv_codes = {l.split("\t")[0] for l in tsv_lines[1:] if l.strip()}

def get_concept(parent_cio: str) -> str:
    parts = parent_cio.split("-")
    return parts[1] if len(parts) > 1 else ""

new_rows = []
for s in all_new_sios:
    if s["code"] in tsv_codes:
        continue
    concept = get_concept(s.get("parent_cio_code",""))
    row = "\t".join([
        s["code"],
        s.get("name",""),
        s.get("description_vi",""),
        "SPECIFIC_IMPL",
        s.get("parent_cio_code",""),
        concept,
        s.get("bloom_level","Apply"),
        s.get("knowledge_dimension","Procedural"),
        "",
    ])
    new_rows.append(row + "\n")

with open(TSV_PATH, "a", encoding="utf-8") as f:
    f.writelines(new_rows)
print(f"[OK] TSV: appended {len(new_rows)} rows")
print(f"\nRun: python3 .agents/skills/tree-validator/scripts/validate_tree.py --project swift-associate")
