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

print(ο('a very long and messy string'))#print for testing 