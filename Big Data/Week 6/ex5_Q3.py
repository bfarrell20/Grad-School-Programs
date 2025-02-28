import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

# Assuming 'paragraph' holds the text of the story
stop_words = set(stopwords.words('english'))

# Tokenize the text
tokens = nltk.word_tokenize(paragraph)

# Remove stopwords
cleaned_tokens = [word for word in tokens if word.lower() not in stop_words]

# Join the cleaned tokens back into a text string
cleaned_text = ' '.join(cleaned_tokens)

import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

from nltk.tokenize import sent_tokenize, word_tokenize

# Assuming 'paragraph' contains the first story text
sent_text = nltk.sent_tokenize(paragraph)  # Tokenize into sentences

# Tokenize each sentence and tag the words with parts of speech
all_tagged = [nltk.pos_tag(nltk.word_tokenize(sent)) for sent in sent_text]

# Tagging the tokens with parts of speech
tagged_words = nltk.pos_tag(tokens)

# Create a dictionary of POS tags and their corresponding words
pos_dict = {}
for word, tag in tagged_words:
    prefix = tag[:2]  # Get the two-letter prefix of the POS tag
    if prefix not in pos_dict:
        pos_dict[prefix] = []
    pos_dict[prefix].append(word)

# Print the dictionary
print(pos_dict)

import pandas as pd

# Create a list of dictionaries for each story (assuming you have multiple stories)
data = []

# Assuming 'story_text' is the cleaned text for one story and 'pos_dict' holds the POS tags
story_row = {
    'story_text': cleaned_text,
    **pos_dict  # Merge the POS dictionary with the story
}

data.append(story_row)

# Create a DataFrame
df = pd.DataFrame(data)

# Print the dataframe
print(df)

# Count occurrences of each POS tag
pos_counts = {tag: len(words) for tag, words in pos_dict.items()}

# Compute total number of words
total_words = len(tokens)

# Compute POS per thousand words
pos_per_thousand = {tag: (count / total_words) * 1000 for tag, count in pos_counts.items()}

# Print POS per thousand words for each story
print(pos_per_thousand)
