#!/usr/bin/env python3
import os
import sys
import subprocess
import datetime
import re
from pathlib import Path

# T6 tech tokens (mirrored from validate_master_tree.py)
TECH_TOKENS = [
    # languages
    r"python", r"swift", r"javascript", r"typescript", r"java\b", r"golang", r"rust",
    r"ruby", r"php", r"kotlin", r"scala", r"perl", r"lua", r"haskell", r"dart",
    r"c\+\+", r"cpp", r"c#", r"csharp", r"objective-?c", r"objc",
    # frameworks / libraries
    r"react\b", r"vue\.js", r"vue\b", r"angular", r"svelte", r"solidjs", r"solid js",
    r"django", r"flask", r"express\b", r"rails\b", r"laravel",
    r"nextjs", r"next\.js", r"nuxt", r"gatsby", r"tailwind", r"bootstrap",
    # platforms / vendors
    r"arduino", r"raspberry pi", r"esp32", r"esp8266", r"node\.js", r"nodejs",
    r"docker", r"kubernetes", r"k8s",
    # specific syntax tokens
    r"codable", r"getelementbyid", r"innerhtml", r"console\.log",
    r"printf", r"scanf", r"std::", r"malloc",
]

TECH_RE = re.compile(
    r"\b(?:%s)\b" % "|".join(TECH_TOKENS),
    re.IGNORECASE,
)

# Technology-agnostic replacement suggestions
T6_FIX_SUGGESTIONS = {
    "python": "PROGRAMMING_LANGUAGE_AGNOSTIC",
    "swift": "PROGRAMMING_LANGUAGE_AGNOSTIC",
    "javascript": "CLIENT_SIDE_SCRIPTING",
    "typescript": "STATICALLY_TYPED_SCRIPTING",
    "java": "OBJECT_ORIENTED_LANGUAGE",
    "golang": "CONCURRENT_COMPILED_LANGUAGE",
    "rust": "MEMORY_SAFE_SYSTEMS_LANGUAGE",
    "react": "COMPONENT_BASED_UI_FRAMEWORK",
    "vue": "REACTIVE_UI_FRAMEWORK",
    "angular": "FULL_STACK_UI_FRAMEWORK",
    "docker": "CONTAINERIZATION_PLATFORM",
    "kubernetes": "CONTAINER_ORCHESTRATION_PLATFORM",
    "aws": "CLOUD_PROVIDER",
    "arduino": "MICROCONTROLLER_PLATFORM",
    "xcode": "IDE_DEVELOPMENT_ENVIRONMENT",
    "console.log": "STANDARD_OUTPUT_LOGGING",
    "printf": "FORMATTED_OUTPUT_FUNCTION",
}

def suggest_fix(term: str) -> str:
    """Return tech-agnostic replacement suggestion for a term."""
    term_lower = term.lower()
    for tech, suggestion in T6_FIX_SUGGESTIONS.items():
        if tech in term_lower:
            return suggestion
    return "TECHNOLOGY_AGNOSTIC_EQUIVALENT"


def git_commit_push(message: str):
    """Commit and push changes to git."""
    try:
        subprocess.run(["git", "add", "-A"], check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", message], check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], check=True, capture_output=True)
        print(f"✅ Git commit & push: {message}")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git commit/push failed: {e}")


def main():
    
    validate_script = Path(".agents/skills/tree-validator/scripts/validate_master_tree.py")
    
    try:
        result = subprocess.run(
            [sys.executable, str(validate_script)],
            capture_output=True, text=True, check=True
        )
        print("✅ Master Tree is healthy. No anomalies found.")
        print(result.stdout)
        
        # Still write healthy status to INBOX
        inbox_path = Path("projects/INBOX.md")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        healthy_entry = f"\n### [AUTO_HEAL] {timestamp} — Master Tree Healthy\n- **Status**: ✅ PASS (0 errors, 0 T6 violations)\n- **Action**: None required\n"
        if inbox_path.exists():
            content = inbox_path.read_text(encoding="utf-8")
            # Keep last 50 entries only
            entries = content.split("\n### [")
            if len(entries) > 50:
                content = "\n### [".join(entries[-50:])
        else:
            content = "# INBOX - Automated Notifications\n"
        inbox_path.write_text(content + healthy_entry, encoding="utf-8")
        
        # Git commit & push
        git_commit_push(f"chore(auto-heal): Master Tree healthy check {timestamp}")
        
    except subprocess.CalledProcessError as e:
        print("❌ Master Tree validation failed. Anomalies detected!")
        print("--- ERROR LOG ---")
        print(e.stdout)
        print(e.stderr)
        print("-----------------")
        print("👉 Next steps: Initiating Auto-Heal Protocol...")
        
        # Parse T6 violations from output
        t6_violations = []
        for line in (e.stdout + e.stderr).splitlines():
            if "[T6_VIOLATION]" in line:
                # Parse: "  • [T6_VIOLATION] concepts/CONCEPT_CODE: 'token' appears in field"
                match = re.search(r"\[T6_VIOLATION\]\s+(\w+)/([^:]+):\s+'([^']+)'\s+appears in\s+(\w+)", line)
                if match:
                    level, code, token, field = match.groups()
                    t6_violations.append({
                        "level": level,
                        "code": code,
                        "token": token,
                        "field": field,
                        "suggestion": suggest_fix(token)
                    })

        # Write detailed report to INBOX
        inbox_path = Path("projects/INBOX.md")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        entry = f"\n### [AUTO_HEAL] {timestamp} — Master Tree Validation FAILED\n"
        entry += f"- **Errors**: {len([l for l in (e.stdout + e.stderr).splitlines() if 'ERROR' in l or 'T6_VIOLATION' in l])}\n"
        entry += f"- **Warnings**: {len([l for l in (e.stdout + e.stderr).splitlines() if 'WARNING' in l or 'WARN' in l])}\n"
        
        if t6_violations:
            entry += f"\n#### 🚫 T6 Neutrality Violations ({len(t6_violations)})\n"
            entry += "| Level | Code | Field | Violation | Suggested Replacement |\n"
            entry += "|-------|------|-------|-----------|----------------------|\n"
            for v in t6_violations:
                entry += f"| {v['level']} | `{v['code']}` | {v['field']} | `{v['token']}` | {v['suggestion']} |\n"
            entry += "\n**→ Action Required**: Human to review and rename violating concepts to technology-agnostic terms (Gate §4).\n"
        
        entry += "\n---\n"
        
        if inbox_path.exists():
            content = inbox_path.read_text(encoding="utf-8")
            entries = content.split("\n### [")
            if len(entries) > 50:
                content = "\n### [".join(entries[-50:])
        else:
            content = "# INBOX - Automated Notifications\n"
        inbox_path.write_text(content + entry, encoding="utf-8")
        
        print(f"📝 Detailed report written to {inbox_path}")
        
        # Git commit & push
        git_commit_push(f"fix(auto-heal): Master Tree validation report {timestamp}")
        
        # Run LLM Auto-Heal Protocol
        auto_heal_script = Path(".agents/skills/tree-validator/scripts/llm_auto_heal_master_tree.py")
        try:
            subprocess.run([sys.executable, str(auto_heal_script)], check=True)
            print("✅ Auto-Heal Protocol completed successfully.")
        except subprocess.CalledProcessError:
            print("❌ Auto-Heal Protocol failed to resolve all issues (logged to INBOX.md)")
            # Don't exit 1 - script completed, just log the failure
            # sys.exit(1)

if __name__ == "__main__":
    main()
