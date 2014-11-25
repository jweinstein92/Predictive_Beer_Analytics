'''
Extracts keywords from beer descriptions obtained from Untappd.
Assigns average weight based on beer ratings.

The dict of keywords is saved to keywords.json in form of:
    beerList['keyword'] = [sumOfRatings, nAppearances]

'''

import nltk
from nltk.corpus import wordnet as wn
import re
import jsonpickle as jpickle
import untappd as UT


def extractKeywords(text):
    keywords = []
    sentences = nltk.sent_tokenize(text)
    words = [nltk.word_tokenize(sent) for sent in sentences]
    words = [nltk.pos_tag(sent) for sent in words]

    # Regex for more precise extraction (?)
    #grammar = "NP: {<DT>?<JJ>*<NN>}"
    #cp = nltk.RegexpParser(grammar)

    for w in words:
        for ww in w:
            # Pick conditions based on word types from nltk
            if (ww[1] == 'NN' or ww[1] == 'JJ') and len(ww[0]) > 3:
                keywords.append(ww[0])
    return keywords
