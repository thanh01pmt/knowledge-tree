import os
import argparse
import json
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Knowledge Researcher - Automated Topic Research")
    parser.add_argument("topic", help="The topic or trend to research (e.g., 'Agentic AI')")
    parser.add_argument("--out-dir", default=".work/research", help="Output directory")
    args = parser.parse_args()

    topic_slug = args.topic.lower().replace(" ", "_").replace("-", "_")
    os.makedirs(args.out_dir, exist_ok=True)
    out_file = os.path.join(args.out_dir, f"{topic_slug}_candidates.md")

    print(f"[*] Starting auto-research for topic: {args.topic}")
    print("[*] Note: In a fully autonomous mode, this script would directly call Exa, Crawl4AI, and last30days APIs.")
    print("[*] For Agentic Execution: The @knowledge-researcher agent will use its MCP tools to perform the following:")
    print(f"    1. Run `last30days` tool with query '{args.topic}'")
    print(f"    2. Run `Exa` search for deep tech articles on '{args.topic}'")
    print(f"    3. Use `Crawl4AI` to extract contents from top 3 URLs")
    print("    4. Synthesize into standard Concepts and Keywords")
    
    # Scaffold the output file
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"# Research Candidates: {args.topic}\n\n")
        f.write(f"Date: {datetime.now().isoformat()}\n\n")
        f.write("## 1. Social & Community Insights (from last30days)\n")
        f.write("<!-- Agent to fill this section -->\n\n")
        f.write("## 2. Deep Tech Articles (from Exa & Crawl4AI)\n")
        f.write("<!-- Agent to fill this section -->\n\n")
        f.write("## 3. Extracted Concepts & Keywords\n")
        f.write("<!-- Agent to list proposed concepts following the 100% Agnostic & Noun Phrase rules -->\n\n")
        f.write("## 4. N:N Mapping Recommendations\n")
        f.write("<!-- Agent to propose which existing Topics/Categories these new concepts belong to -->\n")

    print(f"[+] Scaffolding complete. Candidate file created at: {out_file}")
    print("[+] ACTION REQUIRED: Agent must now execute the tool calls and populate the candidate file.")

if __name__ == "__main__":
    main()
