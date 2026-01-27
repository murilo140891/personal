import pypdf
import sys

def extract_text(pdf_path, output_path):
    reader = pypdf.PdfReader(pdf_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            f.write(f"--- PAGE {page_num + 1} ---\n")
            f.write(text)
            f.write("\n\n")

if __name__ == "__main__":
    extract_text(sys.argv[1], sys.argv[2])
