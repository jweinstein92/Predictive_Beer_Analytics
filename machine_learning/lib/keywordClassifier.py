'''
Show the usage of keywords in various ways.
Write sorted csv and text files for export to database and graphics..
'''

import jsonpickle as jpickle
import sys
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
    keywordsRawDict = jpickle.decode(f)
except:
    print 'Keywords list corrupted'
    sys.exit()
keywordsFile.close()

# Filters - minimum usage and lowercase conversion
votesThreshold = 50
keywordsDict = {k.lower(): v for (k, v) in
                keywordsRawDict.iteritems()
                if (v[1] >= votesThreshold)}

# Dictionary of sorted lists
SortedByRating = {}
SortedByRating['keywords'] = []
SortedByRating['ratings'] = []
SortedByRating['usage'] = []
for word in sorted(keywordsDict.items(),
                   key=lambda k: (k[1][0] / k[1][1]), reverse=True):
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
for word in sorted(keywordsDict.items(),
                   key=lambda k: (k[1][1]), reverse=True):
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

    bars1 = plt.barh(index, SortedByRating['ratings'][0:n],
                     bar_width,
                     alpha=opacity,
                     color='b',
                     error_kw=error_config,
                     label='Rating avg.')

    bars2 = plt.barh(index + bar_width, SortedByRating['usage'][0:n],
                     bar_width,
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

    bars1 = plt.barh(index, SortedByRating['ratings'][-n:],
                     bar_width,
                     alpha=opacity,
                     color='b',
                     error_kw=error_config,
                     label='Rating avg.')

    bars2 = plt.barh(index + bar_width,
                     SortedByRating['usage'][-n:],
                     bar_width,
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

    bars1 = plt.barh(index, [x*1000 for x in SortedByUsage['ratings'][0:n]],
                     bar_width,
                     alpha=opacity,
                     color='b',
                     error_kw=error_config,
                     label='Rating avg. [x1000]')

    bars2 = plt.barh(index + bar_width, SortedByUsage['usage'][0:n],
                     bar_width,
                     alpha=opacity,
                     color='r',
                     error_kw=error_config,
                     label='Usage')

    plt.title('Beer rating keywords')
    plt.yticks(index + bar_width, SortedByUsage['keywords'][0:n])
    plt.legend()
    plt.tight_layout()
    plt.show()


def writeFiles():
    """Export CSV and text files export."""
    f = open('../data/sortedByRating.csv', 'wt')
    writer = csv.writer(f)
    writer.writerow(('id', 'Keyword', 'Rating', 'Usage'))
    for i, word in enumerate(SortedByRating['keywords']):
        try:
            writer.writerow((str(i),
                             word, SortedByRating['ratings'][i],
                             SortedByRating['usage'][i]))
        except:
            pass
    f.close()

    f = open('../data/sortedByUsage.csv', 'wt')
    writer = csv.writer(f)
    writer.writerow(('id', 'Keyword', 'Rating', 'Usage'))
    for i, word in enumerate(SortedByUsage['keywords']):
        try:
            writer.writerow((str(i), word,
                             SortedByUsage['ratings'][i],
                             SortedByUsage['ratings'][i]))
        except:
            pass
    f.close()

    # Files for graphic export to http://www.wordle.net/
    f = open('../data/mostUsedKeywords.txt', 'wt')
    for i, word in enumerate(SortedByUsage['keywords'][0:100]):
        f.write(word + " : " + str(SortedByUsage['usage'][i]) + "\n")
    f.close()

    f = open('../data/bestKeywords.txt', 'wt')
    for i, word in enumerate(SortedByRating['keywords'][0:100]):
        f.write(word + " : " + str(SortedByRating['ratings'][i]*1000) + "\n")
    f.close()

    f = open('../data/worstKeywords.txt', 'wt')
    for i, word in enumerate(SortedByRating['keywords'][100:]):
        f.write(word + " : " + str(SortedByRating['ratings'][i]*1000) + "\n")
    f.close()

plotBestKeywords(10)
plotWorstKeywords(10)
plotMostUsed(40)

writeFiles()

print 'done'
