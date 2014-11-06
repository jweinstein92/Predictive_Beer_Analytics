"""
Extracts keywords from beer descriptions obtained from Untappd.
Assigns average weight based on beer ratings.

The dict of keywords is saved to keywords.json in form of:
    beerList['keyword'] = [sumOfRatings, nAppearances]

"""

import nltk
from nltk.corpus import wordnet as wn
import re


def extractKeywords(text):
    keywords = []
    sentences = nltk.sent_tokenize(text)
    words = [nltk.word_tokenize(sent) for sent in sentences]
    words = [nltk.pos_tag(sent) for sent in words]

    # Regex for more precise extraction (?)
    #grammar = "NP: {<DT>?<JJ>*<NN>}"
    #cp = nltk.RegexpParser(grammar)

    for i in range(len(words)):
        for ii in range(len(words[i])):
            word = words[i][ii]
            # Pick conditions based on word types from nltk
            if (word[1] == 'NN' or word[1] == 'JJ') and len(word[0]) > 3:
                keywords.append(word[0])

    return keywords
