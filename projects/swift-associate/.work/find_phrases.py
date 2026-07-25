import json
import re

# List of verbs provided by the user (case-insensitive)
verbs = [
    "Identify", "Recognize", "Define", "List", "Recall", "State", "Label", "Match",
    "Explain", "Interpret", "Summarize", "Classify", "Compare", "Infer", "Paraphrase",
    "Describe", "Apply", "Calculate", "Compute", "Use", "Solve", "Demonstrate", 
    "Implement", "Execute", "Determine", "Analyze", "Differentiate", "Distinguish", 
    "Contrast", "Organize", "Structure", "Attribute", "Deconstruct", "Outline", 
    "Relate", "Evaluate", "Judge", "Critique", "Justify", "Recommend", "Assess", 
    "Defend", "Prioritize", "Design", "Construct", "Develop", "Formulate", 
    "Propose", "Combine"
]

# Compile a regex pattern to match these verbs at the beginning of a line or after a bullet point
pattern_str = r"^(?:[^a-zA-Z0-9]*\d+\.\d+[^a-zA-Z0-9]*|[^a-zA-Z0-9]+)?(" + "|".join(verbs) + r")\b.*"
regex = re.compile(pattern_str, re.IGNORECASE)

phrases = []
unique_phrases = set()

try:
    with open("projects/swift-associate/.work/kw/chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)
    
    for chunk in chunks:
        text = chunk.get("text", "")
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            match = regex.match(line)
            if match:
                # Deduplicate
                if line not in unique_phrases:
                    unique_phrases.add(line)
                    phrases.append(line)

    print(f"Found {len(phrases)} unique phrases starting with Bloom's Taxonomy verbs:")
    for p in phrases:
        print(f"- {p}")

except Exception as e:
    print(f"Error: {e}")
