from setuptools import setup, find_packages

setup(
      name="PredictiveBeerAnalytics",
      version="0.1",
      packages=find_packages(),
      scripts={'predictiveBeerAnalytics.py','untappd.py', 'PBAMap.py', 'keywordExtractor.py'},
      install_requires={"argparse>=1.2", "jsonpickle>=0.8", "nltk>=3.0", "googlemaps>=1.0.2"},
      package_data={},

      author="Joshua Weinstein, Jim Sundkvist, Marek Kühn",
      description="",
      license="PSF",
      keywords="beer analytics machine learning keyword",
      url=""
)