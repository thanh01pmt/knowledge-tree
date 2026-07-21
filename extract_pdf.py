import sys
from pypdf import PdfReader

def extract(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    with open("projects/swift-associate/.work/raw_pdf.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("Extracted PDF to raw_pdf.txt")

if __name__ == "__main__":
    extract(sys.argv[1])
