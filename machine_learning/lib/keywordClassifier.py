'''
Show the usage of keywords in various ways.
Write sorted csv files. Also for export to database.
'''
import nltk
import jsonpickle as jpickle
import sys
from collections import OrderedDict

import numpy as np
import matplotlib.pyplot as plt
import csv


# Load keywords
try:
    keywordsFile = open('../data/keywords.json', 'rb')
except:
    print 'Keywords.json not found.'
    sys.exit()

try:
    f = keywordsFile.read()
    keywordsDict = jpickle.decode(f)
except:
    keywordsDict = []
    print 'Keywords list corrupted'
    sys.exit()
keywordsFile.close()

# Sorted by average rating
SortedByRating = {}
SortedByRating['keywords'] = []
SortedByRating['ratings'] = []
SortedByRating['usage'] = []
for word in sorted(keywordsDict.items(), key=lambda k: (k[1][0] / k[1][1]), reverse=True):
    ratingSum = word[1][0]
    usage = word[1][1]
    if usage > 2:
        SortedByRating['keywords'].append(word[0])
        SortedByRating['ratings'].append(ratingSum / usage)
        SortedByRating['usage'].append(usage)

# Sorting by keywords usage
SortedByUsage = {}
SortedByUsage['keywords'] = []
SortedByUsage['ratings'] = []
SortedByUsage['usage'] = []
for word in sorted(keywordsDict.items(), key=lambda k: (k[1][1]), reverse=True):
    ratingSum = word[1][0]
    usage = word[1][1]
    SortedByUsage['keywords'].append(word[0])
    SortedByUsage['ratings'].append(ratingSum / usage)
    SortedByUsage['usage'].append(usage)


def plotBestKeywords(n=10):
    """
    Plot a graph of keywords associated with the best rated beers.
    :param n: Amount of keywords.
    """

    fig, ax = plt.subplots()
    index = np.arange(n)

    bar_width = 0.35
    opacity = 0.4
    error_config = {'ecolor': '0.3'}

    bars1 = plt.barh(index, SortedByRating['ratings'][0:n], bar_width,
                     alpha=opacity,
                     color='b',
                     error_kw=error_config,
                     label='Rating avg.')

    bars2 = plt.barh(index + bar_width, SortedByRating['usage'][0:n], bar_width,
                     alpha=opacity,
                     color='r',
                     error_kw=error_config,
                     label='Usage')

    plt.title('Beer rating keywords')
    plt.yticks(index + bar_width, SortedByRating['keywords'][0:n])
    plt.legend()
    plt.tight_layout()
    plt.show()


def plotWorstKeywords(n=10):
    """
    Plot a graph of keywords associated with the worst rated beers.
    :param n: Amount of keywords.
    """

    fig, ax = plt.subplots()
    index = np.arange(n)

    bar_width = 0.35
    opacity = 0.4
    error_config = {'ecolor': '0.3'}

    bars1 = plt.barh(index, SortedByRating['ratings'][-n:], bar_width,
                     alpha=opacity,
                     color='b',
                     error_kw=error_config,
                     label='Rating avg.')

    bars2 = plt.barh(index + bar_width, SortedByRating['usage'][-n:], bar_width,
                     alpha=opacity,
                     color='r',
                     error_kw=error_config,
                     label='Usage')

    plt.title('Beer rating keywords')
    plt.yticks(index + bar_width, SortedByRating['keywords'][-n:])
    plt.legend()
    plt.tight_layout()
    plt.show()

def plotMostUsed(n=10):
    """
    Plot a graph of most used keywords in the beer description.
    :param n: Amount of keywords.
    """

    fig, ax = plt.subplots()
    index = np.arange(n)

    bar_width = 0.35
    opacity = 0.4
    error_config = {'ecolor': '0.3'}

    bars1 = plt.barh(index, [x*1000 for x in SortedByUsage['ratings'][0:n]], bar_width,
                     alpha=opacity,
                     color='b',
                     error_kw=error_config,
                     label='Rating avg. [x1000]')

    bars2 = plt.barh(index + bar_width, SortedByUsage['usage'][0:n], bar_width,
                     alpha=opacity,
                     color='r',
                     error_kw=error_config,
                     label='Usage')

    plt.title('Beer rating keywords')
    plt.yticks(index + bar_width, SortedByUsage['keywords'][0:n])
    plt.legend()
    plt.tight_layout()
    plt.show()

def writeCSV():
    """Export CSV file for import to the database."""
    f = open('../data/sortedByRating.csv', 'wt')
    writer = csv.writer(f)
    writer.writerow( ('id', 'Keyword', 'Rating', 'Usage') )
    for i, word in enumerate(SortedByRating['keywords']):
        try:
            writer.writerow( (str(i), word,SortedByRating['ratings'][i], SortedByRating['usage'][i]))
        except:
            pass
    f.close()

    f = open('../data/sortedByUsage.csv', 'wt')
    writer = csv.writer(f)
    writer.writerow(('id', 'Keyword', 'Rating', 'Usage'))
    for i in range(len(SortedByUsage['keywords'])):
        try:
            writer.writerow((str[i], SortedByUsage['keywords'][i], SortedByUsage['ratings'][i], SortedByUsage['usage'][i]))
        except:
            pass
    f.close()

plotBestKeywords(10)
plotWorstKeywords(10)
plotMostUsed(40)

writeCSV()

print 'done'


