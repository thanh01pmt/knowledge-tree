import sys
with open(".agents/AGENTS.md", "r") as f:
    content = f.read()

old_text = "Định dạng mã SIO: `SIO-<TECH_PREFIX>-<FEATURE_SLUG>` (dạng `UPPER_SNAKE_CASE`)."
new_text = """Định dạng mã CIO và SIO (Semantic Slugs):
   - **CIO:** `CIO-<CONCEPT_CODE>-<SEMANTIC_SLUG>` (dạng `UPPER_SNAKE_CASE`, ngắn gọn 2-4 từ tiếng Anh).
   - **SIO:** `SIO-<TECH_PREFIX>-<SPECIFIC_FEATURE_SLUG>` (dạng `UPPER_SNAKE_CASE`, thể hiện rõ yếu tố đặc thù phân biệt)."""

if old_text in content:
    content = content.replace(old_text, new_text)
    with open(".agents/AGENTS.md", "w") as f:
        f.write(content)
    print("Patched workspace AGENTS.md!")
else:
    print("Old text not found in workspace AGENTS.md!")
