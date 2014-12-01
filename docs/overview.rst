.. Predictive beer analytics documentation master file, created by
   sphinx-quickstart on Mon Dec 01 10:40:00 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Project overview
=====================================================

   
The purpose of this project is to **illustrate various techniques of data mining and machine learning 
using Python** as being taught in course 02819 Data mining using Python at DTU.

By analyzing more than 235.000 user reviews of beers, we managed to create an **algorithm to anticipate the desirability of certain user-defined beer in the specific location**. By doing that, we can for example 
suggest a specific improvement of the beer characteristics to the brewery based on where they want to sell it.

The results are presented in the **interactive web application** along with useful prediction algorithm 
with user-defined parameters.

**Beer characteristics** that matters:

* Beer style
* Alcohol by volume
* Description keywords
* Label colors


Data sources
------------

**UNTAPPD** - social networking service that *"allows its users to check into beers as they drink them, and share these check-ins and their locations with their friends."* (see `here <https://untappd.com/>`_) 

.. note:: 
   For *beer styles, description, label images, Reviews, Location data*

**Google API** - to work with location data.

.. note::
   *Location lookup, state classification, lattitude/longitude lookup.*

**Quantity of data**

.. figure:: quantity.png 
    :height: 400px
    :align: center
    :alt: Quantity of mined data
	
.. note::

	[made Dec 1, 2014] This will increase over time, the api calls are limited.
	
*For easy data update use the main script.*


Technologies used
-----------------

* Web Framework: **Django** (`djangoproject.com <https://www.djangoproject.com/>`_)
* Database: **mySQL** (`mysql.com <http://www.mysql.com/>`_)
* Machine learning: **scikit-learn, Numpy, Scipy, Image-processing** (`scipy.org <http://www.scipy.org/>`_)
* Documentation, code style: **Sphinx, pep8, pep257**

.. image:: logos.png
	:height: 245px
	:align: center

	

