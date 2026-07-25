import sys
import json
import re
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
sys.path.append(".agents/skills/learning-objective-generator/scripts")
from openai import OpenAI

client = OpenAI()
model = "deepseek-v4-flash:cloud"
hlo_dir = Path("projects/swift-associate/.work/hlo")
out_dir = Path("projects/swift-associate/output")

def get_json_block(text):
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1].split("```")[0]
    return text.strip()

def migrate_codes():
    print("Loading current LOs...")
    with open(hlo_dir / "cios.json", "r") as f: cios = json.load(f)
    with open(hlo_dir / "sios.json", "r") as f: sios = json.load(f)
    with open(hlo_dir / "ulos.json", "r") as f: ulos = json.load(f)

    cio_mapping = {}
    cio_prompt = "Dưới đây là danh sách các CIO. Sinh mã code bằng tiếng Anh (SLUG là 2-4 từ, uppercase). Trả về JSON format: {\"mappings\": [{\"old_code\": \"...\", \"new_code\": \"CIO-<CONCEPT_CODE>-<SLUG>\"}]}\n"
    
    print(f"Migrating {len(cios)} CIOs...")
    for i in range(0, len(cios), 50):
        batch = cios[i:i+50]
        # Xóa phần đuôi rác TRUY_C_P để LLM dễ nhận dạng Concept
        text = "\n".join([f"- {c['code']} | Concept: {c.get('parent_ulo_code', '').replace('ULO-', '')} | Name: {c['name']}" for c in batch])
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": cio_prompt + text}]
            )
            raw = get_json_block(resp.choices[0].message.content)
            data = json.loads(raw)
            for item in data.get("mappings", []):
                cio_mapping[item["old_code"]] = item["new_code"]
        except Exception as e:
            print(f"Error on CIO batch {i}: {e}")

    sio_mapping = {}
    sio_prompt = "Dưới đây là danh sách SIO. Sinh mã tiếng Anh chứa đặc thù phân biệt, UPPER_SNAKE_CASE. Trả về JSON: {\"mappings\": [{\"old_code\": \"...\", \"new_code\": \"SIO-SWIFT-<SLUG>\"}]}\n"
    
    print(f"Migrating {len(sios)} SIOs...")
    for i in range(0, len(sios), 50):
        batch = sios[i:i+50]
        text = "\n".join([f"- {s['code']} | Name: {s['name']}" for s in batch])
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": sio_prompt + text}]
            )
            raw = get_json_block(resp.choices[0].message.content)
            data = json.loads(raw)
            for item in data.get("mappings", []):
                sio_mapping[item["old_code"]] = item["new_code"]
        except Exception as e:
            print(f"Error on SIO batch {i}: {e}")

    # Fallback only for remaining
    for c in cios:
        if c["code"] not in cio_mapping:
            print(f"Warning: CIO missing mapping: {c['code']}")
            
    for s in sios:
        if s["code"] not in sio_mapping:
             print(f"Warning: SIO missing mapping: {s['code']}")

    print("Applying mappings to objects...")
    for c in cios:
        if c["code"] in cio_mapping:
            c["code"] = cio_mapping[c["code"]]

    for s in sios:
        if s["code"] in sio_mapping:
            s["code"] = sio_mapping[s["code"]]
        parent_cio = s.get("parent_cio_code", "")
        if parent_cio in cio_mapping:
            s["parent_cio_code"] = cio_mapping[parent_cio]
        parent_lo = s.get("parent_lo_code", "")
        if parent_lo:
            new_parents = []
            for p in parent_lo.replace(";", ",").split(","):
                p = p.strip()
                new_parents.append(cio_mapping.get(p, p))
            s["parent_lo_code"] = ", ".join(new_parents)

    print("Saving changes to JSON files...")
    with open(hlo_dir / "cios.json", "w") as f: json.dump(cios, f, indent=2, ensure_ascii=False)
    with open(hlo_dir / "sios.json", "w") as f: json.dump(sios, f, indent=2, ensure_ascii=False)

    import llm_generate_hierarchical_lo as gen_lo
    with open(out_dir / "concepts_full.tsv", "r", encoding="utf-8") as f:
        concepts = [line.strip().split("\t") for line in f.readlines()[1:]]
    gen_lo.merge_to_tsv(ulos, cios, sios, [{"code": c[0]} for c in concepts], out_dir / "learning-objectives.tsv")
    print("Migration complete!")

if __name__ == "__main__":
    migrate_codes()
