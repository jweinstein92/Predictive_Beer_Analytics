"""
Functions to load downloaded json data.

To do: Make this general.
"""

import jsonpickle as jpickle
import csv
import labels


def readUsers():
    """Load already processed users UntappdUser."""
    try:
        usersFile = open('../data/users.json', 'rb')
    except IOError:
        usersFile = open('../data/users.json', 'wb')

    try:
        f = usersFile.read()
        usersList = jpickle.decode(f)
    except:
        usersList = {}
    usersFile.close()
    return usersList


def readBeers():
    """Load already processed beers UntappdBeer."""
    try:
        beersFile = open('../data/beers.json', 'rb')
    except IOError:
        beersFile = open('../data/beers.json', 'wb')

    try:
        f = beersFile.read()
        beersList = jpickle.decode(f)
    except:
        beersList = {}
    beersFile.close()
    return beersList


def readBreweries():
    """Load already processed breweries UntappdBrewery."""
    try:
        breweriesFile = open('../data/breweries.json', 'rb')
    except IOError:
        breweriesFile = open('../data/breweries.json', 'wb')

    try:
        f = breweriesFile.read()
        breweryList = jpickle.decode(f)
    except:
        breweryList = {}
    breweriesFile.close()
    return breweryList


def readBreweryToBeers():
    """Load already processed breweries dictionary."""
    try:
        breweryToBeersFile = open('../data/breweryToBeers.json', 'rb')
    except IOError:
        breweryToBeersFile = open('../data/breweryToBeers.json', 'wb')

    try:
        f = breweryToBeersFile.read()
        breweryToBeers = jpickle.decode(f)
    except:
        breweryToBeers = {}
    breweryToBeersFile.close()
    return breweryToBeers


def readDataPoints():
    """Load dataPoints."""
    try:
        dataPointsFile = open('../data/dataPoints.json', 'rb')
    except IOError:
        dataPointsFile = open('../data/dataPoints.json', 'wb')

    try:
        f = dataPointsFile.read()
        dataPoints = jpickle.decode(f).points
    except:
        dataPoints = []
    dataPointsFile.close()

    return dataPoints


def readBeerStyles():
    """Load most rated beer styles."""
    styles = []
    with open('../data/styles.csv') as stylesFile:
        reader = csv.DictReader(stylesFile)
        for row in reader:
            if row['style'] not in styles:
                styles.append(row['style'])
    return styles


def readBeerColors():
    """Load the dominant label colors."""
    try:
        beerColorsFile = open('../data/beerColors.json', 'rb')
    except IOError:
        beerColorsFile = open('../data/beerColors.json', 'wb')

    try:
        f = beerColorsFile.read()
        beerColorsDict = jpickle.decode(f)
    except:
        beerColorsDict = labels.BeerColorsDict()
    beerColorsFile.close()
    return beerColorsDict
