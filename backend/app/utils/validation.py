from fuzzywuzzy import fuzz
import re

def validate_citizenship_format(citizenship_number):
    pattern = r'^\d{4}-\d{4}-\d{4}$'
    return bool(re.match(pattern, citizenship_number))

def compare_names(name1, name2, threshold=80):
    ratio = fuzz.ratio(name1.lower(), name2.lower())
    return ratio >= threshold

def validate_dob_format(dob_str):
    patterns = [
        r'^\d{4}-\d{2}-\d{2}$',
        r'^\d{2}/\d{2}/\d{4}$'
    ]
    return any(re.match(pattern, dob_str) for pattern in patterns)
