#!/usr/bin/env python3
"""
full_sync.py — Full sync swift-associate project to Supabase.
Handles:
  1. Core 6 TSVs (fields → learning_objectives) via existing sync_to_supabase.py
  2. concept_learning_objectives  (build from learning-objectives.tsv concept_codes)
  3. lo_prerequisites.tsv         (if exists)
  4. learning_objective_glossaries (keywords.tsv → SIO mapping)

Run AFTER: validate_tree.py PASS, lo_prerequisites.tsv exists.
"""
import csv, json, os, sys, urllib.request
from pathlib import Path

# ─── Setup ────────────────────────────────────────────────────────────────────
REPO = Path(__file__).resolve().parent.parent.parent.parent
OUT  = REPO / "projects/swift-associate/output"

env = {}
with open(REPO / ".env") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()

os.environ.pop("NO_PROXY", None)
os.environ.pop("no_proxy", None)

SUPABASE_URL = env["SUPABASE_URL"]
SERVICE_KEY  = env["SERVICE_ROLE_KEY"]
ORG_CODE     = "DEFAULT_ORG"

HEADERS = {
    "apikey": SERVICE_KEY,
    "Authorization": f"Bearer {SERVICE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates,return=minimal",
}

def supa_upsert(table: str, rows: list[dict]) -> int:
    if not rows:
        return 0
    # Batch in chunks of 500
    total = 0
    for i in range(0, len(rows), 500):
        chunk = rows[i:i+500]
        data = json.dumps(chunk).encode()
        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/{table}",
            data=data,
            headers=HEADERS,
            method="POST",
        )
        try:
            with urllib.request.urlopen(req) as resp:
                total += len(chunk)
        except urllib.error.HTTPError as e:
            err = e.read().decode()
            print(f"  [ERROR] {table}: {e.code} — {err[:200]}")
    return total

def supa_delete_by_org(table: str, org: str):
    """Delete all rows for this org before re-inserting (for junction tables)."""
    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/{table}?organization_code=eq.{org}",
        headers={**HEADERS, "Prefer": ""},
        method="DELETE",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"  Cleared {table} for org={org}")
    except Exception as e:
        print(f"  [WARN] Could not clear {table}: {e}")

print("=" * 60)
print(f"🚀 FULL SYNC — swift-associate → Supabase")
print("=" * 60)

# ─── Step 1: Core 6 TSVs via existing sync script ─────────────────────────────
print("\n[Step 1] Syncing core 6 TSVs (fields → learning_objectives)...")
import subprocess
result = subprocess.run(
    [sys.executable,
     str(REPO / ".agents/skills/supabase-sync/scripts/sync_to_supabase.py"),
     "--project", "swift-associate"],
    capture_output=True, text=True, cwd=str(REPO)
)
print(result.stdout)
if result.returncode != 0:
    print(f"[ERROR] Core sync failed:\n{result.stderr}")
    sys.exit(1)

# ─── Step 2: concept_learning_objectives ──────────────────────────────────────
print("\n[Step 2] Syncing concept_learning_objectives...")

# Load learning-objectives.tsv
with open(OUT / "learning-objectives.tsv", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    los = list(reader)

clo_rows = []
for lo in los:
    code = lo.get("code", "").strip()
    cc = lo.get("concept_codes", "").strip()
    if not code or not cc:
        continue
    concepts = [c.strip() for c in cc.replace(";", ",").split(",") if c.strip()]
    for seq, concept in enumerate(concepts):
        clo_rows.append({
            "concept_code": concept,
            "learning_objective_code": code,
            "organization_code": ORG_CODE,
            "sequence_order": seq,
        })

# Upsert (table has composite PK: concept_code + learning_objective_code + organization_code)
n = supa_upsert("concept_learning_objectives", clo_rows)
print(f"  ✓ concept_learning_objectives: {n} rows upserted ({len(clo_rows)} total)")

# ─── Step 3: learning_objective_prerequisites ──────────────────────────────────
print("\n[Step 3] Syncing lo_prerequisites...")
prereq_file = OUT / "lo_prerequisites.tsv"
if not prereq_file.is_file():
    print("  ⚠️  lo_prerequisites.tsv not found — skipping")
else:
    with open(prereq_file, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        prereq_rows = []
        for r in reader:
            tgt = r.get("learning_objective_code", "").strip()
            pre = r.get("prerequisite_lo_code", "").strip()
            if tgt and pre:
                prereq_rows.append({
                    "learning_objective_code": tgt,
                    "prerequisite_lo_code": pre,
                })
    n = supa_upsert("learning_objective_prerequisites", prereq_rows)
    print(f"  ✓ learning_objective_prerequisites: {n} rows upserted")

# ─── Step 4: learning_objective_glossaries (keyword → SIO) ────────────────────
print("\n[Step 4] Syncing keyword glossaries (learning_objective_glossaries)...")

# Load keywords.tsv — columns: term, aliases, relevance_score, source_chunks, ...
kw_file = OUT / "keywords.tsv"
sio_codes = {lo["code"] for lo in los if lo.get("lo_type","").strip() == "SPECIFIC_IMPL"}

if not kw_file.is_file():
    print("  ⚠️  keywords.tsv not found — skipping")
else:
    with open(kw_file, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        keywords = list(reader)

    # First: upsert glossaries (term → code)
    import re
    def to_code(term: str) -> str:
        return "KW-" + re.sub(r"[^A-Z0-9]", "_", term.upper().strip())[:50].strip("_")

    glos_rows = []
    seen_glos = set()
    for kw in keywords:
        term = kw.get("term", "").strip()
        if not term: continue
        code = to_code(term)
        if code in seen_glos: continue
        seen_glos.add(code)
        glos_rows.append({
            "code": code,
            "name": term[:200],
            "description": kw.get("aliases","")[:500],
            "content": "",
            "organization_code": ORG_CODE,
        })

    n = supa_upsert("glossaries", glos_rows)
    print(f"  ✓ glossaries: {n} rows upserted ({len(glos_rows)} terms)")

    # Build keyword → LO links
    # Strategy: link each keyword to SIOs that mention the keyword term in their description
    with open(OUT / "learning-objectives.tsv", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        sio_rows = [lo for lo in reader if lo.get("lo_type","").strip() == "SPECIFIC_IMPL"]

    lo_glos_rows = []
    seen_pairs = set()
    for sio in sio_rows:
        lo_code = sio.get("code","").strip()
        desc = (sio.get("description","") + " " + sio.get("name","")).lower()
        for kw in keywords:
            term = kw.get("term","").strip()
            if not term: continue
            # Only link if keyword term appears (case-insensitive) in the SIO description
            if len(term) > 4 and term.lower() in desc:
                kw_code = to_code(term)
                pair = (lo_code, kw_code)
                if pair in seen_pairs: continue
                seen_pairs.add(pair)
                lo_glos_rows.append({
                    "learning_objective_code": lo_code,
                    "glossary_code": kw_code,
                })

    n = supa_upsert("learning_objective_glossaries", lo_glos_rows)
    print(f"  ✓ learning_objective_glossaries: {n} rows upserted ({len(lo_glos_rows)} links)")

print("\n" + "=" * 60)
print("🎉 FULL SYNC COMPLETE")
print("=" * 60)

# ─── Final check ──────────────────────────────────────────────────────────────
print("\n[Final] Row counts in Supabase:")
for table in ["learning_objectives", "concept_learning_objectives",
              "learning_objective_prerequisites", "glossaries",
              "learning_objective_glossaries"]:
    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/{table}?select=count",
        headers={**HEADERS, "Prefer": "count=exact"}
    )
    with urllib.request.urlopen(req) as resp:
        cnt = resp.headers.get("Content-Range","?/?").split("/")[-1]
        print(f"  {table:<35} = {cnt} rows")
