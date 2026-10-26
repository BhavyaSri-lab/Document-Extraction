from pypdf import PdfReader
import re
import json
from pathlib import Path

# Step 1: Specify the location of the PDF file
pdf_file = Path("data/lmn-doc-3450_scan.pdf")

# Step 2: Read all the text from the PDF
reader = PdfReader(pdf_file)

text = ""

for page in reader.pages:
    text = text + (page.extract_text() or "")

# Step 3: Search the PDF text for the required details
def find_detail(pattern):
    result = re.search(pattern, text, re.IGNORECASE)

    if result:
        return result.group(1).strip()
    else:
        return None

# Step 4: Store the extracted details in a dictionary
invoice_data = {
    "invoice_number": find_detail(
        r"Invoice No\.?\s*:?\s*([\w/-]+)"
    ),

    "date": find_detail(
        r"Date\s*:?\s*(\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4})"
    ),

    "vendor": find_detail(
        r"FROM\s*\n([^\n]+)"
    ),

    "customer": find_detail(
        r"BILL TO\s*\n([^\n]+)"
    ),

    "total": find_detail(
        r"(?:Grand Total|Total Due)\s*:?\s*₹?\s*([\d,.]+)"
    )
}

# Step 5: Save the JSON file in the same location as the PDF
json_file = pdf_file.with_suffix(".json")

with open(json_file, "w", encoding="utf-8") as file:
    json.dump(invoice_data, file, indent=4)

# Display a success message and the extracted details
print("Invoice details extracted!")
print(invoice_data)