import json
import re #regular expressions
import operator
from collections import Counter
from nltk.corpus import stopwords  #common words
import string


emoticons_str = r"""
      (?:
        [:=;] #Eyes
        [oO\-]? #Nose
        [D\)\]\(\]/\\OpP] #Mouth
      )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

tokens_re = re.compile(r' ('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
        #VERBOSE allows spaces in the regexp to be ignored
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

#catches all tokens in a list and returns as a list
def tokenize(s):
    return tokens_re.findall(s)

def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        #for all elements in the array of token
        #if they satisfy emoticon regex then write that, otherwise lower everything
        #we do this since we don't want smiley face :D to become :d
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens
    
        

punctuation = list(string.punctuation)
stop = stopwords.words('english')+punctuation+['RT', 'rt', 'via', 'Donald', 'Trump', 'gt', 'I', 'https', 'The', "he's", "This", "Is", "I'm", "president", "President", "J"]


with open('python.json', 'r') as f:
    count_all = Counter()  #counts all elements
    for line in f:
        tweet = json.loads(line)
        
        # counts each term in the tweet which is not a stop word
        terms_stop = [term for term in preprocess(tweet['text']) if term not in stop]   
         #update the counter 
        count_all.update(terms_stop)   #keeps frequencies of terms

    #print the first 5 most common words
    #most_common is a predefined method from the library Counter
    print(count_all.most_common(20))
   


