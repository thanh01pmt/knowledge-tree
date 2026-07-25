import sys
with open(".agents/skills/learning-objective-generator/scripts/llm_generate_hierarchical_lo.py", "r") as f:
    content = f.read()

content = content.replace(
    '      "code": "CIO-<CONCEPT_CODE>-<STT>",\n',
    '      "code": "CIO-<CONCEPT_CODE>-<SEMANTIC_SLUG>",\n'
)

content = content.replace(
    '      "code": "SIO-...",\n',
    '      "code": f"SIO-{tech_upper}-<SPECIFIC_FEATURE_SLUG>",\n'
)

with open(".agents/skills/learning-objective-generator/scripts/llm_generate_hierarchical_lo.py", "w") as f:
    f.write(content)
print("Patched!")
