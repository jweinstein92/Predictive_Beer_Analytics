import requests
import json
from ConfigParser import SafeConfigParser


class UntappdUser:
    """
    Representation of an untappd user
    """
    def __init__(self, attribs):
        self.uid = attribs['uid']
        self.username = attribs['username']
        self.location = attribs['location']
        self.ratings = attribs['ratings']


class UntappdBeer:
    """
    Representation of an untappd beer
    """
    def __init__(self, attribs):
        self.bid = attribs['bid']
        self.name = attribs['name']
        self.label = attribs['label']
        self.abv = attribs['abv']
        self.ibu = attribs['ibu']
        self.style = attribs['style']
        self.description = attribs['description']
        self.rating = attribs['rating']
        self.brewery = attribs['brewery']


class UntappdBrewery:
    """
    Representation of an untappd brewery
    """
    def __init__(self, attribs):
        self.breweryId = attribs['breweryId']
        self.name = attribs['name']
        self.label = attribs['label']
        self.country = attribs['country']
        self.location = attribs['location']


class Untappd:
    """
    Untappd object which handles everything related to untappd
    and the data obtained through untappd's api
    """
    def __init__(self):
        self.client_id = ''
        self.client_secret = ''
        self.endpoint = ''
        self.request_header = {}
        self.users = {}
        self.beers = {}
        self.breweries = {}

    def settings(self, filename):
        config = SafeConfigParser()
        config.read(filename)
        client_id = config.get('untappd', 'clientId')
        client_secret = config.get('untappd', 'clientSecret')
        endpoint = config.get('untappd', 'endpoint')
        request_header = {'User-Agent': config.get('untappd', 'header')}

        self.client_id = client_id
        self.client_secret = client_secret
        self.endpoint = endpoint
        self.request_header = request_header

    def createUrl(self, method):
        """
        Creates the api url for the GET request
        """
        return self.endpoint + '/' + method

    def getPubFeed(self):
        """"
        Retrieves information which includes the usernames of
        active members of the site
        """
        method = 'thepub'
        url = self.createUrl(method)
        parameters = {'client_id': self.client_id,
                'client_secret': self.client_secret}
        response = requests.get(url, headers=self.request_header,
                                params=parameters)
        data = json.loads(response.text)
        return data

    def getUserReviewData(self, username, offset):
        method = 'user/beers/' + username
        url = self.createUrl(method)
        parameters = {'offset': offset, 'client_id': self.client_id,
                'client_secret': self.client_secret}
        response = requests.get(url, headers=self.request_header,
                                params=parameters)
        data = json.loads(response.text)
        return data
