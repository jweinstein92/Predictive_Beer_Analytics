.. Predictive beer analytics documentation master file, created by
   sphinx-quickstart on Mon Dec 01 10:40:00 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Getting and Using Data
=====================================================
All data used by this module is mined from the beer review website `Untappd <http://www.untappd.com>`_

To obtain the neccessary data, you must first acquire a **Client Id** and **Client Secrect** key from 
`Untappd API <http://untappd.com/api/docs>`_. Also, a `Google Geocoding API <https://developers.google.com/maps/documentation/geocoding/>`_ key is required. However, the Google Geocoding API limits their keys to 2500 calls a day. If you have more than 2500 users, you will either need multiple keys or will need to change PBAMap.py to handle the usage. These keys must then be placed in the apiConfig.ini located in /machine_learning.

To easily obtain new data, we provided the control script **predictiveBeerAnalytics.py**

Execute::

    $ predictiveBeerAnalytics.py [--users | --reviews | --normalizeData | --keywords |
	--dataPoints | --styles | --abvMap | --styleMap | --colorPalette]
   
Each step adds more to already stored data. It can take hours to collect and analyse the data, 
so we invoke each task separately by choosing one of the arguments.

It is recommended to run the scripts in the following order::

    $ predicitiveBeerAnalytics.py --users
    $ predicitiveBeerAnalytics.py --reviews
    $ predicitiveBeerAnalytics.py --normalizeData
    $ predicitiveBeerAnalytics.py --keywords
    $ predicitiveBeerAnalytics.py --styles
    $ predicitiveBeerAnalytics.py --abvMap <abvAmount>
    $ predicitiveBeerAnalytics.py --styleMap <beerStyle>
    $ predicitiveBeerAnalytics.py --colorPalette

.. automodule:: predictiveBeerAnalytics


User Data (``--users``)
------------------------
In order to effectively use the module, large amounts of data are required. A variety of users from many different places who drink various kinds of beer are ideal. To obtain a useful array of data, lots must be obtained. However, Untappd API limits its developers to only make calls 100 times per hour. To handle this, **predictiveBeerAnalytics.py** pauses the program after every call to ensure that no more than 100 calls are made. It is recommended to leave the script running for long periods of time to obtain data. The script can be run multiple times without losing or duplicating user information, so it can be stopped at any point until a later point.

To mine user data - usernames, locations, and ids::

    $ predictiveBeerAnalytics.py --users

.. warning::
    This is a never ending for loop. User information will continue to be queried until user kills the process with ctrl+C

Beer Data (``--reviews``)
-------------------------
This may only be run if ``--users`` has been previously run as it uses the usernames you have already mined. Each user has their beer ratings queried and returns a maximum of 50 reviews per user. This may be less depending on if they reviewed the same beer multiple times or have not reviewed more than 50 beers. Like ``--users`` it is recommended to leave this script running for long periods of time to obtain data. The more reviews retreived, the better the results will be. This script may be interrupted and restarted.

To mine beer data - user reviews, beer information (name, rating, alcohol content, label, style, description), and brewery information (name, location, beers brewed)::
    
    $ predictiveBeerAnalytics.py --reviews

.. warning::
    This is a never ending for loop. Beer information will continue to be queried until user kills the process with ctrl+C

Normalizing Data (``--normalizeData``)
--------------------------------------
Normalizing the data removes the usernames of users who you have already gathered reviews from. All users with locations are then put through the `Google Geocoding API <https://developers.google.com/maps/documentation/geocoding/>`_ to obtain the longitude and latitude of the users for later use. Due to the daily limit of 2500 calls to the API, it is suggested to get multiple API keys and only have to run this once, opposed to changing code and needing to rerun.

To normalize the data::

    $ predictiveBeerAnalytics.py --normalizeData


Retrieving Description Keywords (``--keywords``)
------------------------------------------------
Having the batch of beers downloaded, this loops over the list, extracts the keywords from each description and attaches it to the dictionary of beers. Tokenized words are then categorized and tagged according to its type using ``nltk`` language processing tool. Primal goal here is to capture the beer characteristics like taste or ingredients. Currently it returns nouns and adjective. The extraction itself is covered by the function located in **keywordExtractor.py**

.. py:function:: extractKeywords(text)
   
   Extract the keywords from any given text.
   
   :param str text: Text subjected to extract from.
   :return: Array of keywords
   
Each keyword is then associated with rating. The rating is calculated as an average of beer ratings possessing this specific keyword. The separate list of keywords is then generated along with the average of ratings of the beers .

To extract keywords and update their ratings::

    $ predictiveBeerAnalytics.py --keywords
	
Reading Beer Styles (``--styles``)
--------------
This looks at all the beers and creates a file of the 20 most reviewed beer styles and stores them in the file styles.csv. This file is then used in ``-stylesMap`` to allow you to create maps based on user reviews and the style of the beer. Other styles may be added to this file, however there probably won't be enough reviews to accurately describe the desirablity of that style in a region.

To create a list of the most rated beer styles::

    $ predictiveBeerAnalytics.py --styles


Creating Maps (``--abvMap`` or ``--styleMap``)
--------------
.. warning::

    Josh please!
	
ColorPalette module
---------------------
This module provides the whole **color processing** functionality. First it looks up the list of all already mined beers and uses the links provided to **download the beer labels** from untappd. With the image size being 100x100 px no additional cropping is required. For reading the image data, we use `imread()` method included ``scipy-misc`` package. For more comprehensive image manipulation and processing ``scikit-image`` would be prefered. However at this point we only need to read the data, so the miscellaneous scikit package is sufficient. 

Once all the labels are downloaded, the **clustering** is performed on each of them. For that we use `K-Means clustering <http://en.wikipedia.org/wiki/K-means_clustering>`_ algorithm provided by `sklearn.cluster  
<http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html>`_ module. 

The clustered colors are then **categorized** to fit the color palette and averaged beer rating for those colors are derived. The array of rated colors is the output we want. 

To trigger this module use::

    $ predictiveBeerAnalytics.py --colorPalette

