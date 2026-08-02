#!/usr/bin/env python3
"""
agent_as_judge.py — Independent Semantic Evaluator for Automated Pipelines.

This script acts as the "Agent-as-Judge" to replace Human-in-the-Loop at key
checkpoint stages. It evaluates artifacts for semantic correctness,
hallucinations, T6 neutrality violations, and pedagogical quality.

Supported stages:
  - mapping_plan: Evaluate mapping-plan.md before /build-tree
  - ulo: Evaluate generated ULOs for Bloom level, neutrality, coverage
  - cio: Evaluate generated CIOs for Marr 2-Language compliance

Usage:
  python3 agent_as_judge.py --artifact <path> --stage mapping_plan
  python3 agent_as_judge.py --artifact <path> --stage ulo --context <path_to_concepts.tsv>
  python3 agent_as_judge.py --artifact <path> --stage cio
"""

import argparse
import csv
import json
import os
import sys
from pathlib import Path

# Setup path for shared LLM call
_SKILL_SCRIPTS = Path(__file__).resolve().parents[2] / "keyword-extractor" / "scripts"
if str(_SKILL_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SKILL_SCRIPTS))

try:
    from llm_call import llm_chat_json, LLMCallError
except ImportError:
    print(f"[ERROR] Could not import llm_call from {_SKILL_SCRIPTS}", file=sys.stderr)
    sys.exit(1)

try:
    from openai import OpenAI
except ImportError:
    print("[ERROR] Please install openai: pip install openai", file=sys.stderr)
    sys.exit(1)

# ── Tech-specific terms blacklist for T6 check (rule-based layer) ──────────
_TECH_BLACKLIST = [
    "React", "Vue", "Angular", "Svelte", "Next.js", "Nuxt",
    "Swift", "Kotlin", "Python", "Java", "JavaScript", "TypeScript",
    "Go", "Rust", "Ruby", "PHP", "Dart", "C#", "C++",
    "Docker", "Kubernetes", "AWS", "Azure", "GCP",
    "Django", "Flask", "Express", "Laravel", "Spring",
    "TensorFlow", "PyTorch", "Codable", "SwiftUI", "UIKit",
    "Raspberry Pi", "Arduino", "ESP32",
    "Node.js", "Deno", "Bun",
    "MongoDB", "PostgreSQL", "MySQL", "Redis",
    "getElementById", "innerHTML",
]


def _rule_based_t6_check(content: str) -> list[str]:
    """Quick regex-free scan for technology-specific terms in neutral layers."""
    violations = []
    for term in _TECH_BLACKLIST:
        if term.lower() in content.lower():
            violations.append(f"T6 violation: '{term}' found in artifact content")
    return violations


def _read_artifact(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"[ERROR] Artifact not found: {path}", file=sys.stderr)
        sys.exit(1)


def _save_approved(artifact_path: Path, content: str) -> Path:
    approved_path = artifact_path.parent / f"{artifact_path.stem}-approved{artifact_path.suffix}"
    approved_path.write_text(content, encoding="utf-8")
    print(f"[SUCCESS] Agent-as-Judge approved. Saved to: {approved_path}")
    return approved_path


def evaluate_mapping_plan(client, model: str, artifact_path: Path):
    """Evaluate mapping-plan.md for T6 neutrality and structural validity."""
    print(f"\n{'='*60}")
    print(f"[JUDGE] Stage: MAPPING_PLAN")
    print(f"[JUDGE] Artifact: {artifact_path}")
    print(f"{'='*60}")

    content = _read_artifact(artifact_path)

    # Layer 1: Rule-based T6 scan
    rule_violations = _rule_based_t6_check(content)
    if rule_violations:
        print(f"\n[JUDGE] Rule-based T6 scan found {len(rule_violations)} violation(s):")
        for v in rule_violations:
            print(f"  • {v}")

    # Layer 2: LLM semantic evaluation
    system_prompt = """You are an independent AI Judge evaluating a Taxonomy Mapping Plan.
Your job: strict review + auto-correct. Return a JSON object with these keys:
- "is_approved": boolean (true if plan is valid or you successfully fixed all issues)
- "feedback": string (detailed critique listing errors found)
- "corrected_content": string (the full corrected markdown; if no fixes needed, return original)

Evaluation criteria:
1. T6 NEUTRALITY: All Concepts/Topics/Categories must be 100% technology-agnostic.
   NO specific languages/frameworks/tools (React, Python, Swift, Docker, etc.).
   [NEW NODE PROPOSAL] with tech names → rewrite to generic concepts.
2. HALLUCINATION CHECK: Any concept codes referenced must look like valid UPPER_SNAKE_CASE.
3. STRUCTURAL VALIDITY: Markdown structure must be logical and complete.
4. COVERAGE: Every syllabus section should map to at least one concept.

If violations exist, fix them in corrected_content and explain in feedback."""

    user_prompt = f"""Evaluate and auto-correct this mapping plan. Return JSON only.

{content}"""

    try:
        result = llm_chat_json(client, model, system_prompt, user_prompt, temperature=0.1)
    except LLMCallError as e:
        print(f"[FATAL] LLM Judge failed: {e}", file=sys.stderr)
        sys.exit(1)

    feedback = result.get("feedback", "No feedback.")
    is_approved = result.get("is_approved", False)
    corrected = result.get("corrected_content", content)

    print(f"\n--- Judge Feedback ---\n{feedback}\n{'─'*40}")

    if not is_approved:
        print("[REJECTED] Mapping plan failed evaluation.", file=sys.stderr)
        sys.exit(1)

    return _save_approved(artifact_path, corrected)


def evaluate_ulos(client, model: str, artifact_path: Path, context_path: str = None):
    """Evaluate generated ULOs for Bloom level distribution and T6 neutrality."""
    print(f"\n{'='*60}")
    print(f"[JUDGE] Stage: ULO EVALUATION")
    print(f"[JUDGE] Artifact: {artifact_path}")
    print(f"{'='*60}")

    content = _read_artifact(artifact_path)

    # Layer 1: Rule-based T6 scan
    rule_violations = _rule_based_t6_check(content)
    if rule_violations:
        print(f"\n[JUDGE] Rule-based T6 scan found {len(rule_violations)} violation(s):")
        for v in rule_violations:
            print(f"  • {v}")

    # Layer 2: LLM semantic evaluation
    system_prompt = """You are an independent AI Judge evaluating Universal Learning Objectives (ULOs).
Return a JSON object with keys: "is_approved" (bool), "feedback" (str), "corrected_content" (str).

Evaluation criteria:
1. T6 NEUTRALITY: ULO names and descriptions must be 100% technology-agnostic.
   They cannot mention specific languages, frameworks, or tools.
2. BLOOM LEVEL DISTRIBUTION: ULOs should favor higher-order Bloom levels
   (Evaluate, Create, Analyze) over lower ones (Remember, Understand).
   Flag if >60% of ULOs are at Remember/Understand level.
3. DESCRIPTION PREFIX: Every ULO description MUST start with "Người học có khả năng ..."
4. ASSESSMENT APPROACH: Each ULO must have a non-empty assessment_approach.
5. CONCEPT COVERAGE: Check that ULOs collectively cover the breadth of concepts provided.

Fix violations in corrected_content. Explain issues in feedback."""

    user_prompt = f"""Evaluate these ULOs. Return JSON only.

{content}"""

    try:
        result = llm_chat_json(client, model, system_prompt, user_prompt, temperature=0.1)
    except LLMCallError as e:
        print(f"[FATAL] LLM Judge failed: {e}", file=sys.stderr)
        sys.exit(1)

    feedback = result.get("feedback", "No feedback.")
    is_approved = result.get("is_approved", False)
    corrected = result.get("corrected_content", content)

    print(f"\n--- Judge Feedback ---\n{feedback}\n{'─'*40}")

    if not is_approved:
        print("[REJECTED] ULOs failed evaluation.", file=sys.stderr)
        sys.exit(1)

    return _save_approved(artifact_path, corrected)


def evaluate_cios(client, model: str, artifact_path: Path):
    """Evaluate generated CIOs for Marr 2-Language Test compliance."""
    print(f"\n{'='*60}")
    print(f"[JUDGE] Stage: CIO EVALUATION (Marr Test)")
    print(f"[JUDGE] Artifact: {artifact_path}")
    print(f"{'='*60}")

    content = _read_artifact(artifact_path)

    # Layer 1: Rule-based T6 scan
    rule_violations = _rule_based_t6_check(content)
    if rule_violations:
        print(f"\n[JUDGE] Rule-based T6 scan found {len(rule_violations)} violation(s):")
        for v in rule_violations:
            print(f"  • {v}")

    # Layer 2: LLM semantic evaluation with Marr Test focus
    system_prompt = """You are an independent AI Judge evaluating Conceptual Implementation Objectives (CIOs).
Return a JSON object with keys: "is_approved" (bool), "feedback" (str), "corrected_content" (str).

Evaluation criteria:
1. MARR 2-LANGUAGE TEST (Critical): Each CIO MUST be representation-independent.
   Test: Can the CIO description be naturally mapped to ≥2 different languages/tools?
   If a CIO's wording only fits one specific language's syntax (e.g., token ordering
   specific to Python/Swift), it has been DEMOTED to Implementational level → REWRITE.
2. T6 NEUTRALITY: CIO names and descriptions must be 100% technology-agnostic.
3. DESCRIPTION PREFIX: Every CIO description MUST start with "Người học có khả năng ..."
4. PARENT LINKAGE: Each CIO must reference valid parent ULO codes.
5. ASSESSMENT APPROACH: Each CIO must have a non-empty assessment_approach.

Fix violations in corrected_content. Explain issues in feedback.
For Marr violations, rewrite the CIO to be procedurally neutral, or recommend demotion to SIO."""

    user_prompt = f"""Evaluate these CIOs. Return JSON only.

{content}"""

    try:
        result = llm_chat_json(client, model, system_prompt, user_prompt, temperature=0.1)
    except LLMCallError as e:
        print(f"[FATAL] LLM Judge failed: {e}", file=sys.stderr)
        sys.exit(1)

    feedback = result.get("feedback", "No feedback.")
    is_approved = result.get("is_approved", False)
    corrected = result.get("corrected_content", content)

    print(f"\n--- Judge Feedback ---\n{feedback}\n{'─'*40}")

    if not is_approved:
        print("[REJECTED] CIOs failed Marr Test evaluation.", file=sys.stderr)
        sys.exit(1)

    return _save_approved(artifact_path, corrected)


def main():
    parser = argparse.ArgumentParser(
        description="Agent-as-Judge: Independent Semantic Evaluator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python3 agent_as_judge.py --artifact .work/mapping-plan.md --stage mapping_plan
  python3 agent_as_judge.py --artifact .work/phase_ulos.json --stage ulo
  python3 agent_as_judge.py --artifact .work/phase_cios.json --stage cio"""
    )
    parser.add_argument("--artifact", required=True,
                        help="Path to the artifact file to judge")
    parser.add_argument("--stage", required=True,
                        choices=["mapping_plan", "ulo", "cio"],
                        help="Pipeline stage to evaluate")
    parser.add_argument("--context", default=None,
                        help="Optional context file (e.g. concepts.tsv for ULO coverage check)")
    parser.add_argument("--model", default="gpt-4o",
                        help="OpenAI model (default: gpt-4o)")
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print("[ERROR] OPENAI_API_KEY not found.", file=sys.stderr)
        sys.exit(1)

    base_url = os.environ.get("OPENAI_BASE_URL")
    client = OpenAI(api_key=api_key, base_url=base_url)

    artifact_path = Path(args.artifact)

    if args.stage == "mapping_plan":
        evaluate_mapping_plan(client, args.model, artifact_path)
    elif args.stage == "ulo":
        evaluate_ulos(client, args.model, artifact_path, args.context)
    elif args.stage == "cio":
        evaluate_cios(client, args.model, artifact_path)


if __name__ == "__main__":
    main()
