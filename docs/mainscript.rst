.. Predictive beer analytics documentation master file, created by
   sphinx-quickstart on Mon Dec 01 10:40:00 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Getting new data
=====================================================
All data used by this module is mined from the beer review website `Untappd <http://www.untappd.com>`_

To obtain the neccessary data, you must first acquire a **Client Id** and **Client Secrect** key from 
`Untappd API <http://untappd.com/api/docs>`_. Also, a `Google Geocoding API <https://developers.google.com/maps/documentation/geocoding/>`_ key is required. However, the Google Geocoding API limits their keys to 2500 calls a day. If you have more than 2500 users, you will either need multiple keys or will need to change PBAMap.py to handle the usage. These keys must then be placed in the apiConfig.ini located in /machine_learning.

To easily obtain new data, we provided the control script **predictiveBeerAnalytics.py**

Execute::

    $ predictiveBeerAnalytics.py [--users | --reviews | --normalizeData | --keywords |
	--dataPoints | --styles | --abvMap | --styleMap | --colorPalette]
   
Each step adds more to already stored data. It can take hours to collect and analyze the data, 
so we invoke each task separately by choosing one of the arguments.

It is reccommended to run the scripts in the following order::

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


Retreiving Description Keywords (``--keywords``)
------------------------------------------------
.. warning::

	Marek please!
	
Reading Beer Styles (``--styles``)
--------------
.. warning::

	Josh please!

Creating Maps (``--abvMap`` or ``--styleMap``)
--------------
.. warning::

    Josh please!
	
ColorPalette module
---------------------
.. warning::

	Marek please!

*
