import string

def get_afinn_bad_words(input_file, output_file):
    bad_words = set()
    with open(input_file, 'r') as file:
        for line in file:
            if not line.strip():
                continue
            parts = line.strip().split()
            if len(parts) == 2:
                word, score_str = parts
                try:
                    score = int(score_str)
                    if score in {-4, -5}:
                        # Remove punctuation from the word
                        word_clean = word.translate(str.maketrans('', '', string.punctuation))
                        bad_words.add(word_clean.lower())
                except ValueError:
                    continue

    # Write to file, one word per line
    with open(output_file, 'w') as out:
        for word in sorted(bad_words):
            out.write(f"{word}\n")

# Example usage
if __name__ == '__main__':
    afinn_path = 'AFN.txt'  # Replace with your actual AFINN file path
    output_path = 'bad_words.txt'
    get_afinn_bad_words(afinn_path, output_path)
    print(f"Saved bad words to {output_path}")
