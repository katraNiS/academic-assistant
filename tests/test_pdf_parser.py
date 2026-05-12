import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag.pdf_parser import extract_text_from_pdf


test_pdf = Path("corpus/pdfs/1401.0942v2.pdf")  # δικό σου path

text = extract_text_from_pdf(test_pdf)

print(f"Total length: {len(text)} chars\n")
print("=== First 500 chars ===")
print(text[:500])
print("\n=== Last 500 chars ===")
print(text[-500:])

print("\n\n=== Batch test ===")
from src.rag.pdf_parser import extract_all_pdfs

results = extract_all_pdfs("corpus/metadata.json")
print(f"\nExtracted {len(results)} papers")

# Spot check: πάρε ένα τυχαίο id και δες πόσοι χαρακτήρες
first_id = list(results.keys())[0]
print(f"\nFirst paper ({first_id}): {len(results[first_id])} chars")