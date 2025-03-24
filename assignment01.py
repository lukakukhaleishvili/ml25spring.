from difflib import SequenceMatcher

def most_similar_sequence(new_seq, existing_seqs):
    best_match = None
    highest_ratio = 0
    
    for seq in existing_seqs:
        similarity = SequenceMatcher(None, new_seq, seq).ratio()
        if similarity > highest_ratio:
            highest_ratio = similarity
            best_match = seq
    
    return best_match, highest_ratio


existing_sequences = ["abcdef", "abcfed", "ghijkl", "abcde"]
new_sequence = "abcdf"

best_match, similarity = most_similar_sequence(new_sequence, existing_sequences)
print(f"ყველაზე მსგავსი მიმდევრობა: {best_match} (მსგავსება: {similarity:.2f})")
