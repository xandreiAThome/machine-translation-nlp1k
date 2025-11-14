import regex as re
import nltk
import pandas as pd
from pathlib import Path

def clean_string(input_string):
    """Remove non-alphabetic characters except whitespace and convert to lowercase."""
    cleaned = re.sub(r"[^\p{L}\s]", "", input_string.strip().lower())
    return cleaned

def tokenize_text(text):
    """Tokenize text using NLTK word_tokenize. Returns empty list for missing verses."""
    if text is None or text.strip() == "" or text.lower() == "<no verse>":
        return []
    
    try:
        tokens = nltk.word_tokenize(text)
        return tokens
    except LookupError:
        # Fallback to simple whitespace tokenization if punkt not available
        return text.split()

def preprocess_parallel_tsv(tsv_file, source_col, target_col, output_dir="data/aligned", prefix=""):
    # Read TSV file
    df = pd.read_csv(tsv_file, sep='\t')
    
    # Initialize lists for aligned pairs
    source_tokens_list = []
    target_tokens_list = []
    skipped = 0
    
    # Process each row
    for idx, row in df.iterrows():
        source_text = row[source_col]
        target_text = row[target_col]
        
        # Check for missing verses
        if pd.isna(source_text) or pd.isna(target_text):
            skipped += 1
            continue
        
        source_str = str(source_text).strip()
        target_str = str(target_text).strip()
        
        if source_str.lower() == "<no verse>" or target_str.lower() == "<no verse>":
            skipped += 1
            continue
        
        if source_str == "" or target_str == "":
            skipped += 1
            continue
        
        # Clean and tokenize
        source_cleaned = clean_string(source_str)
        target_cleaned = clean_string(target_str)
        
        # Skip if cleaning results in empty strings
        if not source_cleaned or not target_cleaned:
            skipped += 1
            continue
        
        source_tokens = tokenize_text(source_cleaned)
        target_tokens = tokenize_text(target_cleaned)
        
        # Only add if both have tokens
        if source_tokens and target_tokens:
            source_tokens_list.append(source_tokens)
            target_tokens_list.append(target_tokens)
    
    print(f"Processed {len(df)} verses from {tsv_file}")
    print(f"  Valid aligned pairs: {len(source_tokens_list)}")
    print(f"  Skipped (missing/empty verses): {skipped}")
    
    return source_tokens_list, target_tokens_list

def save_aligned_corpus(source_tokens, target_tokens, output_dir="data/aligned", prefix=""):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Save source and target separately
    source_file = Path(output_dir) / f"{prefix}source.txt"
    target_file = Path(output_dir) / f"{prefix}target.txt"
    
    with open(source_file, 'w', encoding='utf-8') as f:
        for tokens in source_tokens:
            f.write(' '.join(tokens) + '\n')
    
    with open(target_file, 'w', encoding='utf-8') as f:
        for tokens in target_tokens:
            f.write(' '.join(tokens) + '\n')
    
    print(f"Saved {len(source_tokens)} aligned pairs to:")
    print(f"  Source: {source_file}")
    print(f"  Target: {target_file}")
