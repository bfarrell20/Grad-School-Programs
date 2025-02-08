import os
import re
import requests
from sklearn.feature_extraction.text import TfidfVectorizer

# Given code
stop_url = "https://gist.githubusercontent.com/rg089/35e00abf8941d72d419224cfd5b5925d/raw/12d899b70156fd0041fa9778d657330b024b959c/stopwords.txt"
stopwords_list = requests.get(stop_url).content
stopwords = set(stopwords_list.decode().splitlines())

def remove_stopwords(text):
    words = re.sub(r"[^a-zA-Z0-9]", " ", text.lower()).split()
    return " ".join([word for word in words if word not in stopwords])

def load_speeches(directory): #method to get all the speeches for a specific president
    texts = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                    texts.append(remove_stopwords(f.read()))
    return texts

def compute_tfidf(speeches):#method to compute the tfidf for the speeches
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(speeches)
    feature_names = vectorizer.get_feature_names_out()
    
    avg_tfidf = tfidf_matrix.mean(axis=0).A1
    word_tfidf = dict(zip(feature_names, avg_tfidf))
    
    return sorted(word_tfidf.items(), key=lambda x: x[1], reverse=True)[:15]

if __name__ == "__main__":
    lincoln_folder = "lincoln"  # Chose lincoln 
    
    speeches = load_speeches(lincoln_folder)
    top_words = compute_tfidf(speeches)
    
    print("Top 15 most important words in Lincoln's speeches:")
    for word, score in top_words:
        print(f"{word}: {score:.4f}")
