import pytesseract
from PIL import Image
import re

def extract_citizenship_data(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    
    data = {
        'name': None,
        'citizenship_number': None,
        'dob': None
    }
    
    # Extract citizenship number (format: 1234-5678-9012 or similar)
    citizenship_pattern = r'\d{4}[-\s]?\d{4}[-\s]?\d{4}'
    citizenship_match = re.search(citizenship_pattern, text)
    if citizenship_match:
        data['citizenship_number'] = citizenship_match.group().replace(' ', '-')
    
    # Extract DOB (format: YYYY-MM-DD or DD/MM/YYYY)
    dob_pattern = r'\d{4}[-/]\d{2}[-/]\d{2}|\d{2}[-/]\d{2}[-/]\d{4}'
    dob_match = re.search(dob_pattern, text)
    if dob_match:
        data['dob'] = dob_match.group()
    
    # Extract name (basic heuristic - first capitalized line)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    for line in lines:
        if line[0].isupper() and len(line.split()) >= 2:
            data['name'] = line
            break
    
    return data, text
