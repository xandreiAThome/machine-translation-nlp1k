def test_alignment(source_file,target_file,align_file,verse_index):
    # Read all lines into lists
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            source_sents = [line.strip().split() for line in f] # Split into words
        
        with open(target_file, 'r', encoding='utf-8') as f:
            target_sents = [line.strip().split() for line in f] # Split into words
            
        with open(align_file, 'r', encoding='utf-8') as f:
            alignments = [line.strip() for line in f]
    except FileNotFoundError as e:
        print(f"Error: Could not find file {e.filename}")
        return

    if verse_index >= len(source_sents):
        print(f"Error: Index {verse_index} is out of bounds.")
        return
        
    source_words = source_sents[verse_index]
    target_words = target_sents[verse_index]
    align_string = alignments[verse_index]
    
    # 'align_string' looks like "0-0 1-2 2-1"
    # We turn it into a dictionary: {0: [0], 1: [2], 2: [1]}
    links = {}
    if align_string: # Make sure it's not empty
        for pair in align_string.split():
            s, t = map(int, pair.split('-'))
            if s not in links:
                links[s] = []
            links[s].append(t)

    print(f"\nSource : {' '.join(source_words)}")
    print(f"Target : {' '.join(target_words)}")
    
    linked_found = False
    for source_index, source_word in enumerate(source_words):
        if source_index in links:
            linked_found = True
            # Get all target words linked to this source word
            target_indices = links[source_index]
            target_word_list = [target_words[i] for i in target_indices]
            
            print(f" src: '{source_word}'  ->  trgt: {target_word_list}")
        
    if not linked_found:
        print("No alignments found for this sentence.")