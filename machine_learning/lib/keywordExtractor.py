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

def ExtractKeywords(text):
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
            if (word[1]=='NN' or word[1]=='JJ') and len(word[0])>3:
                keywords.append(word[0])

    return keywords

# Load untappd beers
try:
    beersFile = open('../data/beers.json', 'rb')
    #beersFile = open('beers_sample.json', 'rb')
except IOError:
    beersFile = open('../data/beers.json', 'wb')
    #beersFile = open('beers_sample.json', 'wb')
try:
    f = beersFile.read()
    beersList = jpickle.decode(f)
except:
    beersList = []
beersFile.close()
print 'beers.json LOADED...'

# List of keywords generation
keywordsList = {}
position = 0

for id, beer in beersList.iteritems():
    beer.keywords=[]
    beer.keywords=ExtractKeywords(beer.description)
    for keyword in beer.keywords:
        if keyword in keywordsList:
            keywordsList[keyword][0] += beer.rating
            keywordsList[keyword][1] += 1
        else:
            keywordsList[keyword]=[beer.rating, 1]
    position += 1
    if (position % 100)==0:
        print 'Processed ' + str(position) + '/' + str(beersList.__len__()) + ' beers. '

with open('../data/beers.json','wb') as beersFile:
    json = jpickle.encode(beersList)
    beersFile.write(json)

with open('../data/keywords.json', 'wb') as keywordsFile:
    json = jpickle.encode(keywordsList)
    keywordsFile.write(json)

