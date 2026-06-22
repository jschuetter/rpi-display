'''
Helper module to read liturgical calendar PDFs
'''

import sys, os
from pathlib import Path
from pypdf import PdfReader

if len(sys.argv) < 2: 
    print("Please provide the path of a PDF file to parse")
    sys.exit()

reader = PdfReader(os.path.join(
        Path(__file__).resolve().parents[0], # Get path to module directory
        'resources',
        sys.argv[1]
        ))

calendar_object = []
page_idx = 0
first_word = ""
while first_word != "YEAR":
    page_idx += 1
    page = reader.pages[page_idx]
    page_text = page.extract_text().split()
    first_word = page_text[1] if len(page_text) > 1 else None
    print(page_idx)
    print(page_text)

start_page = page_idx

for page_idx in range(start_page, len(reader.pages)):
    page = reader.pages[page_idx]
    page_text = page.extract_text()
    for line in page_text.split('\n'): 
        print(line)