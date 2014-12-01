"""
Single-purpose script for easy monitoring of data quantity.

Load each json data file, find its size and generate
a plot for presentation.
"""

import fileReader as files
import matplotlib.pyplot as plt
import os
import numpy as np

# Load files
print "Loading beers..."
beersList = files.readBeers()
print "Loading users..."
usersList = files.readUsers()
print "Loading breweries..."
breweriesList = files.readBreweries()

# Path for saving the images
path = "../data/labels/"
fileList = os.listdir(path)

# Data gathering
labels = ('Beers', 'Reviews', 'Users', 'Breweries', 'Labels')
index = np.arange(len(labels))
quantities = (len(beersList), sum([len(x.ratings) for x in usersList.values()]),
               len(usersList),  len(breweriesList), len(fileList))

# Plot the quantities
plt.figure(1)
bar_width = 0.35
opacity = 0.7

bars = plt.bar(index, quantities,
                 bar_width,
                 alpha=opacity,
                 color='g')

plt.xticks(index + bar_width/2, labels)
plt.title('Amount of mined data')
plt.ylabel('log(N)')
plt.yscale('log')
plt.grid()

def autoLabel(bars):
    # attach some text labels
    for rect in bars:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')

autoLabel(bars)
plt.show()