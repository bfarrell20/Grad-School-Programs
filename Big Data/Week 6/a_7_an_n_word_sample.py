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
    "The sun was shining on the sea,
      Shining with all his might:
He did his very best to make
      The billows smooth and bright —
And this was odd, because it was
      The middle of the night.

The moon was shining sulkily,
      Because she thought the sun
Had got no business to be there
      After the day was done —
"It's very rude of him," she said,
      "To come and spoil the fun."

The sea was wet as wet could be,
      The sands were dry as dry.
You could not see a cloud, because
      No cloud was in the sky:
No birds were flying overhead —
      There were no birds to fly.

The Walrus and the Carpenter
      Were walking close at hand;
They wept like anything to see
      Such quantities of sand:
If this were only cleared away,'
      They said, it would be grand!'

If seven maids with seven mops
      Swept it for half a year,
Do you suppose,' the Walrus said,
      That they could get it clear?'
I doubt it,' said the Carpenter,
      And shed a bitter tear.

O Oysters, come and walk with us!'
      The Walrus did beseech.
A pleasant walk, a pleasant talk,
      Along the briny beach:
We cannot do with more than four,
      To give a hand to each.'

The eldest Oyster looked at him,
      But never a word he said:
The eldest Oyster winked his eye,
      And shook his heavy head —
Meaning to say he did not choose
      To leave the oyster-bed.

But four young Oysters hurried up,
      All eager for the treat:
Their coats were brushed, their faces washed,
      Their shoes were clean and neat —
And this was odd, because, you know,
      They hadn't any feet.

Four other Oysters followed them,
      And yet another four;
And thick and fast they came at last,
      And more, and more, and more —
All hopping through the frothy waves,
      And scrambling to the shore.

The Walrus and the Carpenter
      Walked on a mile or so,
And then they rested on a rock
      Conveniently low:
And all the little Oysters stood
      And waited in a row.

The time has come,' the Walrus said,
      To talk of many things:
Of shoes — and ships — and sealing-wax —
      Of cabbages — and kings —
And why the sea is boiling hot —
      And whether pigs have wings.'

But wait a bit,' the Oysters cried,
      Before we have our chat;
For some of us are out of breath,
      And all of us are fat!'
No hurry!' said the Carpenter.
      They thanked him much for that.

A loaf of bread,' the Walrus said,
      Is what we chiefly need:
Pepper and vinegar besides
      Are very good indeed —
Now if you're ready, Oysters dear,
      We can begin to feed.'

But not on us!' the Oysters cried,
      Turning a little blue.
After such kindness, that would be
      A dismal thing to do!'
The night is fine,' the Walrus said.
      Do you admire the view?

It was so kind of you to come!
      And you are very nice!'
The Carpenter said nothing but
      Cut us another slice:
I wish you were not quite so deaf —
      I've had to ask you twice!'

It seems a shame,' the Walrus said,
      To play them such a trick,
After we've brought them out so far,
      And made them trot so quick!'
The Carpenter said nothing but
      The butter's spread too thick!'

I weep for you,' the Walrus said:
      I deeply sympathize.'
With sobs and tears he sorted out
      Those of the largest size,
Holding his pocket-handkerchief
      Before his streaming eyes.

O Oysters,' said the Carpenter,
      You've had a pleasant run!
Shall we be trotting home again?'
      But answer came there none —
And this was scarcely odd, because
      They'd eaten every one."

    """
    cleaned_poem = ο(poem)
    for word in cleaned_poem.split():
        yield word

def sample_words(sample_size, word_num):
    """Returns a tuple of size sample_size after word_num words have been received."""
    random.seed(2025)  # Ensure consistency and repeatability
    gen = word_generator()
    
    
    # Collect the next sample_size words
    sampled = [next(gen, None) for _ in range(sample_size)]
    return tuple(sampled)

# Example usage
if __name__ == "__main__":
    print(sample_words(10, 10))
