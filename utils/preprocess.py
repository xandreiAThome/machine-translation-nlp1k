import regex as re
import nltk

def clean_string(input_string):
    cleaned = re.sub(r"[^\p{L}\s]", "", input_string.strip().lower())
    return cleaned
