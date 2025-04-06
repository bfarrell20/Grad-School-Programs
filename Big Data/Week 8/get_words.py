def get_afinn_bad_words(filepath):
    bad_words = set()
    with open(filepath, 'r') as file:
        for line in file:
            if not line.strip():
                continue
            parts = line.strip().split()
            if len(parts) == 2:
                word, score_str = parts
                try:
                    score = int(score_str)
                    if score == -4 or score == -5:
                        bad_words.add(word)
                except ValueError:
                    pass  # skip lines with invalid scores
    return bad_words

# Example usage
if __name__ == '__main__':
    afinn_path = 'AFN.txt'  # Change this to your actual file path
    severe_neg_words = get_afinn_bad_words(afinn_path)
    print(f"Words with sentiment -4 or -5 ({len(severe_neg_words)} words):")
    print(sorted(severe_neg_words))
