'''
    Download, process label images for all beers.
    i.e. Assign N most used colors based on K-Means clustering algorithm

    Create a custom color palette with ratings.
'''

import os
import numpy as np
import numpy.ma as ma  # Masked array
import matplotlib.pyplot as plt
import matplotlib.cm as cm  # Color map
from sklearn.cluster import KMeans
from scipy import misc
from math import sqrt
import requests


class Image:
    """
    Object to manipulate image data and cluster the colors.
    """

    def __init__(self, imgFilePath):
        self.filePath = imgFilePath
        self.raw_data = misc.imread(imgFilePath)

        # Normalizing RGB to be in the range [0-1]. Assuming 8bit integer coding.
        self.original_data = np.array(self.raw_data, dtype=np.float64) / 255
        #self.original_data = np.array(self.raw_data, dtype=np.float64)

        # Transform to a 2D numpy array [100x100px - no need to crop].
        self.w, self.h, self.d = self.shape = tuple(self.raw_data.shape)
        self.shape1d = (self.w, self.h, 1)
        assert self.d == 3  # [R,G,B] tuple

        # Arrays for further manipulation
        self.pixels = np.reshape(self.original_data, (self.w * self.h, self.d))
        self.kmeans = None
        self.nColors = 0
        self.mask = Mask(self)

        # Convert to grayscale for analysis (cropping etc.)
        self.grayscale = np.zeros(self.shape1d)
        for i, row in enumerate(self.original_data):
            for j, color in enumerate(row):
                r, g, b = tuple(color)
                # Uses luminosity method - better match with human perception
                self.grayscale[i][j] = 0.21 * r + 0.72 * g + 0.07 * b

    def preprocess(self):
        """Prepare image for the clustering."""

        # Check if the picture has white background [sample 5x5], otherwise do not crop
        offsetFromWhite = sqrt(sum(np.array([x * x for x in (1 - self.original_data[0:5, 0:5])]).flatten()))
        if offsetFromWhite > 0.05:
            return

        # Cropping based on luminiscence derivative
        # looks for the first jump from the sides and makes flags for generating mask
        lightDifference = np.zeros(self.shape1d)
        for r, row in enumerate(self.grayscale):
            borderDetected = False
            for c, col in enumerate(row):
                if c < (self.w - 1):
                    diff = self.grayscale[r][c + 1][0] - self.grayscale[r][c][0]
                    lightDifference[r, c] = diff

                    # Border detection from the left side
                    if abs(diff) > 0.05 and borderDetected == False:
                        self.mask.boundaries[r, c] = 1
                        borderDetected = True

            # Border detection from the right side
            c = self.w - 1
            borderDetected = False
            while c > 0:
                diff = lightDifference[r, c]
                if abs(diff) > 0.05 and borderDetected == False:
                    self.mask.boundaries[r, c] = 1
                    borderDetected = True
                c -= 1

        self.mask.genMatrix()

    def clusterize(self, n):
        """Cluster the image into [n] of RGB Clusters using Scikit KMeans class."""
        self.nColors = n

        # Apply cropping mask if exists
        try:
            pixels = np.reshape(ma.masked_array(self.pixels, mask=self.mask.matrix), (self.w * self.h, self.d))
        except:
            pixels = self.pixels

        # Calculate the clusters
        self.kmeans = KMeans(init='k-means++', n_clusters=n, random_state=0).fit(pixels)

        return BeerColor(self.kmeans)

    def quantizeImage(self):
        """Plot the image using only clustered colors."""

        codeBook = self.kmeans.cluster_centers_

        # Determine to which cluster the pixel belongs
        labels = self.kmeans.predict(self.pixels)

        newImage = np.zeros((self.w, self.h, self.d))
        label_idx = 0
        for i in range(self.w):
            for j in range(self.h):
                newImage[i][j] = codeBook[labels[label_idx]]
                label_idx += 1
        self.pixels = newImage

    def showResults(self):
        """Plot the original picture, processed picture and clustered colors"""
        plt.figure(1)
        plt.clf()

        plt.subplot(2, 2, 1)
        plt.title('Original')

        plt.imshow(self.original_data)
        plt.axis('scaled')

        plt.subplot(2, 2, 2)
        plt.title('Quantized')
        plt.imshow(self.pixels)
        plt.axis('scaled')

        plt.subplot(2, 2, 3)
        plt.title('Mask')
        plt.imshow(self.mask.matrix)
        plt.axis('scaled')

        plt.subplot(2, 2, 4)
        plt.title('Cluster colors')
        for i, color in enumerate(self.kmeans.cluster_centers_):
            rectangleHeight = self.h / self.nColors
            rectangleWidth = rectangleHeight
            rectangle = plt.Rectangle((i * rectangleWidth, 0), rectangleWidth, rectangleHeight, fc=color)
            plt.gca().add_patch(rectangle)
        plt.axis('scaled')
        plt.show()


class Mask:
    """Object to handle non-rectangular color-difference based cropping."""
    def __init__(self, img):
        self.w, self.h, self.d = self.shape = img.shape
        self.boundaries = np.zeros(self.shape)
        self.matrix = np.zeros(self.shape)

    def genMatrix(self):
        for r, row in enumerate(self.boundaries):
            # From the left
            c = 0
            while row[c][0] == 0 and c < self.w - 1:
                self.matrix[r][c] = (1, 1, 1)
                c += 1
            # From the right
            c = self.w - 1
            while row[c][0] == 0 and c > 0:
                self.matrix[r][c] = (1, 1, 1)
                c -= 1


class ColorPalette:
    """
    Object to create color palette from already processed
    beer labels.
    """
    def __init__(self):
        # self.nColors = nPaletteColors
        self.palette = dict()

    def build(self, beerColorsDict, beersList):
        print 'Generating the color palette... '

        # colorSamples = beerColorsDict.getColors()
        #
        # # Calculate the clusters
        # kmeans = KMeans(init='k-means++', n_clusters=self.nColors, random_state=0).fit(colorSamples)
        #
        # # Construct the Palette
        # for i in range(self.nColors):
        #     paletteColor = self.palette[i] = dict()
        #     paletteColor['RGB'] = kmeans.cluster_centers_[i].tolist()
        #     paletteColor['RatingSum'] = 0
        #     paletteColor['Occurrences'] = 0
        #     paletteColor['Rating'] = 0
        #
        # # Assign colorPalette flags to the dictionary of beerColors
        # for bid, beerColor in beerColorsDict.iteritems():
        #     i = 0
        #     beer = getBeer(bid, beersList)
        #     if beer:
        #         for color in beerColor.colors:
        #             # Lookup and append the flag
        #             beerColor.colorPaletteFlags[i] = flag =  kmeans.labels_[np.where(colorSamples == color)[0][0]].tolist()
        #             self.palette[flag]['Occurrences'] += 1
        #             self.palette[flag]['RatingSum'] += beer.rating
        #             i += 1
        #     else:
        #         print 'Not found bid ' + bid
        #
        # for color in self.palette.values():
        #     if color['Occurrences'] != 0:
        #         color['Rating'] = color['RatingSum']/color['Occurrences']

        webPaletteRGB = [[254, 82, 9],
                         [251, 153, 2],
                         [247, 189, 1],
                         [255, 254, 53],
                         [209, 233, 51],
                         [102, 177, 49],
                         [2, 145, 205],
                         [9, 68, 253],
                         [63, 1, 164],
                         [134, 2, 172],
                         [168, 24, 75],
                         [254, 38, 18],
                         [255, 255, 255],
                         [0, 0, 0]]

        # Normalize
        webPaletteRGB = (np.array(webPaletteRGB, dtype=np.float64)/255).tolist()

        # Construct the Palette
        for i in range(len(webPaletteRGB)):
            paletteColor = self.palette[i] = dict()
            paletteColor['RGB'] = webPaletteRGB[i]
            paletteColor['RatingSum'] = 0
            paletteColor['Occurrences'] = 0
            paletteColor['Rating'] = 0

        progress = Progress(max=len(beerColorsDict), msg="Rating the  colors from palette... ")
        for bid, beerColor in beerColorsDict.iteritems():
            beer = getBeer(bid, beersList)
            if beer:
                for colorId, beerColorValue in enumerate(beerColor.colors):
                    closestPaletteColorId =  self.classifyColor(beerColorValue)

                    # Update classification flags
                    beerColor.colorPaletteFlags[colorId] = closestPaletteColorId

                    # Update color rating
                    self.palette[closestPaletteColorId]['RatingSum'] += beer.rating
                    self.palette[closestPaletteColorId]['Occurrences'] += 1
            else:
                print 'Not found bid ' + bid

            # Show the classified color.
            # plt.figure(1)
            # plt.title('Palette colors')
            # color = [beerColor.colors[colorId], self.palette[closestPaletteColorId]['RGB']]
            # for i in range(2):
            #     rectangleHeight = 20
            #     rectangleWidth = 20
            #     rectangle = plt.Rectangle((i * rectangleWidth, 0), rectangleWidth, rectangleHeight, fc=color[i])
            #     plt.gca().add_patch(rectangle)
            # plt.axis('scaled')
            # plt.show()

            progress.tick()

        for color in self.palette.values():
            if color['Occurrences'] != 0:
                color['Rating'] = color['RatingSum']/color['Occurrences']


    def classifyColor(self, inputColor):
        closestDistance = sqrt(3)
        inputColorYUV = RGBtoYUV(inputColor)
        for paletteColorId, paletteColor in self.palette.iteritems():
            # Find maximum Euclidean distance of linear colorspace (YUV) values
            paletteColorYUV = RGBtoYUV(paletteColor['RGB'])
            distance = sqrt((paletteColorYUV[0] - inputColorYUV[0])**2 +
                            (paletteColorYUV[1] - inputColorYUV[1])**2 +
                            (paletteColorYUV[2] - inputColorYUV[2])**2)
            if distance < closestDistance:
                closestDistance = distance
                closestPaletteColorId = paletteColorId

        return closestPaletteColorId


class BeerColor:
    """Object to save dominant colors of beer along with the color palette flags."""
    def __init__(self, kmeans):
        self.colors = kmeans.cluster_centers_.tolist()  # array of RGB values
        self.presence = [(float(sum(kmeans.labels_ == i)) / kmeans.labels_.size)
                         for i in range(len(kmeans.cluster_centers_))]
        self.colorPaletteFlags = [0] * len(self.colors)


class BeerColorsDict(dict):
    def __init__(self, *arg, **kw):
        super(BeerColorsDict, self).__init__(*arg, **kw)

    def getColors(self):
        """Return non-nested color RGB values for K-Means processing."""
        return np.concatenate([x for x in [i.colors for i in self.values()]])


class Progress:
    """Print percentage of done work."""
    def __init__(self, max, msg="Processing... ", freq=100):
        self.max = max
        self.msg = msg
        self.printFrequency = max/freq   # Each percent
        self.i = 0

    def tick(self):
        """Call in every cycle."""
        if (self.i % self.printFrequency) == 0:
            print self.msg + str(100*self.i/self.max) + "%"
        if self.i == self.max:
            print "Done."
        self.i += 1


def download(beersList, imgPath, fileList):
    """Gets the beer Labels based on the  Untapped beer list."""
    progress = Progress(max=len(beersList), msg="Downloading images... ")
    for hashId, beer in beersList.iteritems():
        url = beer.label
        if url and (url != 'https://d1c8v1qci5en44.cloudfront.net/site/assets/images/temp/badge-beer-default.png'):
            fileType = url.split("/")[-1].split(".")[-1]
            filePath = imgPath + str(beer.bid) + '.' + fileType
            fileName = str(beer.bid) + '.' + fileType
            if fileName not in fileList:
                r = requests.get(url, stream=True)
                if r.status_code == 200:
                    with open(filePath, 'wb') as f:
                        for chunk in r.iter_content(1024):
                            f.write(chunk)
        progress.tick()


def getBeer(bid, beersList):
    """Search for beer based on bid"""
    for beer in beersList.values():
        if beer.bid == bid:
            return beer
    return None


def unique_rows(a):
    a = np.ascontiguousarray(a)
    unique_a = np.unique(a.view([('', a.dtype)]*a.shape[1]))
    return unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))


def RGBtoYUV(RGB):
    '''Convert array of RGB values to YUV colorspace.'''
    T = np.matrix('0.299 0.587 0.114;'
                  '-0.14713 -0.28886 0.436;'
                  '0.615 -0.51499 -0.10001')
    try:
        return T*np.transpose(np.matrix(RGB))
    except:
        print "Unable to convert RGB -> YUV."
        return 0
