import requests
import json
import csv
from time import sleep

"""
Predictive Beer Analytics script which retrieves the usernames of active members of Untappd.com
"""

client_id = 'ADD'
client_secret = 'ADD'
endpoint = 'http://api.untappd.com/v4'
requestHeader = {'User-Agent': 'ADD'}


def createUrl(method):
	"""
	Creates the api url for the GET request
	"""
	return endpoint + '/' + method

def getPubFeed():
	""""
	Retrieves information which includes the usernames of active members of the site
	"""
	method = 'thepub'
	url = createUrl(method)
	parameters = {'client_id': client_id, 'client_secret': client_secret}
	response = requests.get(url,headers=requestHeader, params=parameters)
	data = json.loads(response.text)
	return data


def main():
	"""
	Parses through data from /thepub to get unique usernames and user ids. Stores this information
	in a csv file to be used in later api requests
	"""
	usernames = dict()
	with open('userInfo.csv', 'a+') as usernameFile:
		reader = csv.reader(usernameFile)
		# read the previously written usernames so there are no duplicates if script run multiple times
		for row in reader:
			uid = row[0]
			usernames[uid] = row[1]

	apiCount = 0
	userNameCountAdditions = 0
	with open('userInfo.csv', 'ab') as usernameFile:
		writer = csv.writer(usernameFile)
		while (True):
			# get 25 most recent updates
			data = getPubFeed()
			apiCount += 1
			print 'apiCount: ' + str(apiCount)
			checkins = data['response']['checkins']['items']
			# each response has 25 items, each with a username
			for checkin in checkins:
				userId = checkin['user']['uid']
				username = checkin['user']['user_name']
				userLocation = checkin['user']['location']
				if str(userId) not in usernames:
					userNameCountAdditions += 1
					writer.writerow((userId, username, unicode(userLocation).encode("utf-8")))
					usernames[str(userId)] = username
			# Untappd only allows 100 api requests per hour. Sleep for 40 seconds between requests
			sleep(38)

main()
	