import random
import re, string, requests
stopwords_list = requests.get("https://gist.githubusercontent.com/rg089/35e00abf8941d72d419224cfd5b5925d/raw/12d899b70156fd0041fa9778d657330b024b959c/stopwords.txt").content
stopwords = list(set(stopwords_list.decode().splitlines()))

def ο(text, is_recursive=False):
    if not is_recursive:
        text = text.lower()
        text = re.sub(r'\[.*?\]', '', text)
        text = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', text)
        text = re.sub(r'[\d]+', ' ', text)
        text = ' '.join(remove_stopwords(text))
        return ο(text, is_recursive=True)
    else:
        # Base case
        return text

def remove_stopwords(words):
    list_ = re.sub(r'[^a-zA-Z0-9]', " ", words.lower()).split()
    return [itm for itm in list_ if itm not in stopwords]

def word_generator():
    """Yields words from the poem one at a time."""
    poem = """
    The sun was shining on the sea,
    Shining with all his might:
    He did his very best to make
    The billows smooth and bright —
    And this was odd, because it was
    The middle of the night.
    
    The Walrus and the Carpenter
    Were walking close at hand;
    They wept like anything to see
    Such quantities of sand:
    "If this were only cleared away,"
    They said, "it would be grand!"
    
    "O Oysters, come and walk with us!"
    The Walrus did beseech.
    A pleasant walk, a pleasant talk,
    Along the briny beach:
    We cannot do with more than four,
    To give a hand to each.
    
    "The eldest Oyster looked at him,
    But never a word he said:
    The eldest Oyster winked his eye,
    And shook his heavy head —
    Meaning to say he did not choose
    To leave the oyster-bed.
    
    "Out four young Oysters hurried up,
    All eager for the treat:
    Their coats were brushed, their faces washed,
    Their shoes were clean and neat —
    And this was odd, because, you know,
    They hadn't any feet.
    
    "Four other Oysters followed them,
    And yet another four;
    And thick and fast they came at last,
    And more, and more, and more —
    All hopping through the frothy waves,
    And scrambling to the shore.
    
    They’d eaten every one.
    """
    
    cleaned_poem = ο(poem)
    for word in cleaned_poem.split():
        yield word

def sample_words(sample_size, word_num):
    """Returns a tuple of size sample_size after word_num words have been received."""
    random.seed(2025)  # Ensure consistency and repeatability
    gen = word_generator()
    
    # Skip the first word_num words
    for _ in range(word_num):
        next(gen, None)
    
    # Collect the next sample_size words
    sampled = [next(gen, None) for _ in range(sample_size)]
    return tuple(sampled)

# Example usage
if __name__ == "__main__":
    print(sample_words(5, 10))
