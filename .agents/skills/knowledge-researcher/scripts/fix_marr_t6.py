#!/usr/bin/env python3
"""
fix_marr_t6.py — Fix Marr T6 violations in Master Tree TSV

Replaces technology-specific terms with technology-agnostic equivalents.
"""

import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[4]  # knowledge-tree root
TSV_PATH = ROOT_DIR / ".agents" / "skills" / "taxonomy-mapper" / "resources" / "mlo-knowlege-tree.tsv"
STAGING_PATH = ROOT_DIR / "services" / "python-api" / "general-context" / "mlo-knowlege-tree.tsv"

# Replacement mappings: (old_term) -> (new_term, reason)
REPLACEMENTS = {
    # Arduino → Microcontroller
    "Arduino": ("microcontroller", "Generic embedded platform"),
    "arduino": ("microcontroller", "Generic embedded platform"),
    "ARDUINO": ("MICROCONTROLLER", "Generic embedded platform"),
    
    # JavaScript → Client-side scripting / ECMAScript
    "JavaScript": ("client-side scripting", "Language-agnostic web scripting"),
    "javascript": ("client-side scripting", "Language-agnostic web scripting"),
    "JAVASCRIPT": ("CLIENT-SIDE SCRIPTING", "Language-agnostic web scripting"),
    
    # React → Component-based frontend framework
    "React": ("component-based frontend framework", "Pattern-agnostic UI framework"),
    "react": ("component-based frontend framework", "Pattern-agnostic UI framework"),
    "REACT": ("COMPONENT-BASED FRONTEND FRAMEWORK", "Pattern-agnostic UI framework"),
    
    # Vue → Progressive frontend framework
    "Vue": ("progressive frontend framework", "Pattern-agnostic UI framework"),
    "vue": ("progressive frontend framework", "Pattern-agnostic UI framework"),
    "VUE": ("PROGRESSIVE FRONTEND FRAMEWORK", "Pattern-agnostic UI framework"),
    
    # Angular → Full-featured frontend framework
    "Angular": ("full-featured frontend framework", "Pattern-agnostic UI framework"),
    "angular": ("full-featured frontend framework", "Pattern-agnostic UI framework"),
    "ANGULAR": ("FULL-FEATURED FRONTEND FRAMEWORK", "Pattern-agnostic UI framework"),
    
    # Swift → Native mobile language
    "Swift": ("native mobile language", "Platform-agnostic mobile development"),
    "swift": ("native mobile language", "Platform-agnostic mobile development"),
    "SWIFT": ("NATIVE MOBILE LANGUAGE", "Platform-agnostic mobile development"),
    "SwiftUI": ("declarative UI framework", "Pattern-agnostic UI framework"),
    "swiftui": ("declarative UI framework", "Pattern-agnostic UI framework"),
    
    # Unity → Game engine
    "Unity": ("game engine", "Generic real-time 3D engine"),
    "unity": ("game engine", "Generic real-time 3D engine"),
    "UNITY": ("GAME ENGINE", "Generic real-time 3D engine"),
    
    # Roblox → User-generated content platform
    "Roblox": ("user-generated content platform", "Generic UGC gaming platform"),
    "roblox": ("user-generated content platform", "Generic UGC gaming platform"),
    "ROBLOX": ("USER-GENERATED CONTENT PLATFORM", "Generic UGC gaming platform"),
    
    # Photoshop → Raster graphics editor
    "Photoshop": ("raster graphics editor", "Generic image manipulation software"),
    "photoshop": ("raster graphics editor", "Generic image manipulation software"),
    "PHOTOSHOP": ("RASTER GRAPHICS EDITOR", "Generic image manipulation software"),
    
    # Django → Full-stack web framework
    "Django": ("full-stack web framework", "Pattern-agnostic web framework"),
    "django": ("full-stack web framework", "Pattern-agnostic web framework"),
    "DJANGO": ("FULL-STACK WEB FRAMEWORK", "Pattern-agnostic web framework"),
    
    # AWS → Cloud provider
    "AWS": ("cloud provider", "Generic cloud infrastructure"),
    "aws": ("cloud provider", "Generic cloud infrastructure"),
    
    # Azure → Cloud provider
    "Azure": ("cloud provider", "Generic cloud infrastructure"),
    "azure": ("cloud provider", "Generic cloud infrastructure"),
    "AZURE": ("CLOUD PROVIDER", "Generic cloud infrastructure"),
    
    # Python → General-purpose language
    "Python": ("general-purpose language", "Language-agnostic programming"),
    "python": ("general-purpose language", "Language-agnostic programming"),
    "PYTHON": ("GENERAL-PURPOSE LANGUAGE", "Language-agnostic programming"),
    
    # Spring → Enterprise application framework
    "Spring": ("enterprise application framework", "Pattern-agnostic backend framework"),
    "spring": ("enterprise application framework", "Pattern-agnostic backend framework"),
    "SPRING": ("ENTERPRISE APPLICATION FRAMEWORK", "Pattern-agnostic backend framework"),
}

# Fields to process for replacements
FIELDS_TO_FIX = ["name", "description", "keywords", "cs2023_ka_mapping", "metadata"]


def fix_tsv_content(content: str) -> tuple:
    """Apply Marr T6 fixes to TSV content. Returns (fixed_content, changes_made)."""
    lines = content.splitlines()
    changes = []
    
    # Find header row to get column indices
    headers = None
    header_idx = -1
    for i, line in enumerate(lines):
        if line.startswith("code\t") and "name" in line:
            headers = line.split("\t")
            header_idx = i
            break
    
    if not headers:
        return content, changes
    
    # Map field names to column indices
    field_indices = {}
    for idx, h in enumerate(headers):
        h_clean = h.strip().lower()
        if h_clean in [f.lower() for f in FIELDS_TO_FIX]:
            field_indices[h_clean] = idx
    
    # Process data rows
    for i in range(header_idx + 1, len(lines)):
        line = lines[i]
        if not line.strip() or line.startswith("Bảng") or line.startswith("Mỗi") or line.startswith("Đây là") or line.startswith("Các"):
            continue
        if line.startswith("|") and "code" not in line:
            continue
        
        parts = line.split("\t")
        if len(parts) < len(headers):
            continue
        
        row_changed = False
        row_changes = []
        
        for field, idx in field_indices.items():
            if idx < len(parts):
                original = parts[idx]
                fixed = original
                
                # Apply replacements
                for old_term, (new_term, reason) in REPLACEMENTS.items():
                    if old_term in fixed:
                        fixed = fixed.replace(old_term, new_term)
                        row_changes.append(f"  {field}: '{old_term}' → '{new_term}' ({reason})")
                        row_changed = True
                
                if row_changed:
                    parts[idx] = fixed
        
        if row_changed:
            lines[i] = "\t".join(parts)
            code = parts[0] if parts else "unknown"
            changes.append(f"Row {i+1} (code={code}):")
            changes.extend(row_changes)
    
    return "\n".join(lines), changes


def main():
    print(f"[*] Loading Master Tree from: {TSV_PATH}")
    
    if not TSV_PATH.exists():
        print(f"[!] File not found: {TSV_PATH}")
        sys.exit(1)
    
    content = TSV_PATH.read_text(encoding="utf-8")
    print(f"[*] Loaded {len(content)} chars, {len(content.splitlines())} lines")
    
    # Apply fixes
    print("[*] Applying Marr T6 fixes...")
    fixed_content, changes = fix_tsv_content(content)
    
    if not changes:
        print("[*] No changes needed - already compliant!")
        return
    
    print(f"[*] Found {len(changes)} changes across {len([c for c in changes if c.startswith('Row')])} rows")
    
    # Backup original
    backup_path = TSV_PATH.with_suffix(".tsv.marr-t6-backup")
    TSV_PATH.rename(backup_path)
    print(f"[*] Backed up original to: {backup_path}")
    
    # Write fixed version
    TSV_PATH.write_text(fixed_content, encoding="utf-8")
    print(f"[+] Fixed TSV written to: {TSV_PATH}")
    
    # Also update staging copy if exists
    if STAGING_PATH.exists():
        STAGING_PATH.write_text(fixed_content, encoding="utf-8")
        print(f"[+] Staging copy updated: {STAGING_PATH}")
    
    # Print changes summary
    print("\n=== CHANGES SUMMARY ===")
    for change in changes:
        print(change)
    
    # Count violations fixed
    violation_terms = set()
    for old_term in REPLACEMENTS.keys():
        if old_term.lower() in content.lower():
            violation_terms.add(old_term)
    print(f"\n[*] Total violation term types found: {len(violation_terms)}")
    print(f"[*] Terms: {', '.join(sorted(violation_terms))}")


if __name__ == "__main__":
    main()