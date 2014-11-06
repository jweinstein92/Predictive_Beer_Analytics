# coding=utf-8
from setuptools import setup, find_packages
from ez_setup import use_setuptools

use_setuptools()
setup(
      name="PredictiveBeerAnalytics",
      version="0.1",
      packages=find_packages(),
      scripts={'lib/predictiveBeerAnalytics.py','lib/untappd.py', 'lib/PBAMap.py', 'lib/keywordExtractor.py'},
      install_requires={"argparse>=1.2", "jsonpickle>=0.8", "nltk>=3.0", "googlemaps>=1.0.2"},

      author="Joshua Weinstein, Jim Sundkvist, Marek Kühn",
      description="",
      license="PSF",
      keywords="beer analytics machine learning keyword",
      url=""
)