import requests
import json
import csv
import mysql.connector


class UntappdUser:
    def __init__(self, attribs):
        self.uid = attribs['uid']
        self.username = attribs['username']
        self.location = attribs['location']
        self.ratings = attribs['ratings']


class UntappdBeer:
    def __init__(self, attribs):
        self.name = attribs['name']
        self.label = attribs['label']
        self.abv = attribs['abv']
        self.ibu = attribs['ibu']
        self.style = attribs['style']
        self.description = attribs['description']
        self.rating = attribs['rating']
        self.brewery = attribs['brewery']


class UntappdBrewery:
    def __init__(self, attribs):
        self.name = attribs['name']
        self.label = attribs['label']
        self.country = attribs['country']
        self.location = attribs['location']


class Untappd:
    def __init__(self):
        self.client_id = ''
        self.client_secret = ''
        self.endpoint = ''
        self.request_header = {}
        self.users = []
        self.beers = []
        self.breweries = []

    def settings(self, filename):
        with open(filename, 'rb') as settings:
            reader = csv.reader(settings)
            for row in reader:
                client_id = row[0]
                client_secret = row[1]
                endpoint = row[2]
                request_header = {'User-Agent': row[3]}
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


def normalizeUsers(userList):
    i = 1
    for user in userList:
        user.uid = str(i)
        del user.username
        i += 1
    return userList

# class DatabaseObject:
#     def __init__(self):
#         self.db_config = dict()

#     def config(self, configFile):
#         with open(configFile, 'rb') as config:
#             reader = csv.reader(config)
#             for row in reader:
#                 user = row[0]
#                 password = row[1]
#                 host = row[2]
#                 database = row[3]
#             self.db_config = {
#                 'user': user,
#                 'password': password,
#                 'host': host,
#                 'database': database,
#                 'raise_on_warnings': True
#             }

#     def dataToDatabase(self, data):
#         print self.db_config
#         cnx = mysql.connector.connect(**self.db_config)
#         cursor = cnx.cursor()
#         print 'hello'
