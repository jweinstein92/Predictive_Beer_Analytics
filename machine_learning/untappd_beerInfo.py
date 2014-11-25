import requests
import json
import csv
import pickle
from time import sleep

client_id = 'ADD'
client_secret = 'ADD'
endpoint = 'http://api.untappd.com/v4'
requestHeader = {'User-Agent': 'ADD'}

def createUrl(method):
	return endpoint + '/' + method

def getUserReviewData(username, offset):
	method = 'user/beers/' + username
	url = createUrl(method)
	parameters = {'offset': offset, 'client_id': client_id, 'client_secret': client_secret}
	response = requests.get(url,headers=requestHeader, params=parameters)
	data = json.loads(response.text)
	return data



def main():
	# load already processed users dictionary
	usersFile = open('users.pkl', 'rb')
	try:
		users = pickle.load(usersFile)
	except:
		users = dict()
	usersFile.close()

	# load already processed beers dictionary
	beersFile = open('beers.pkl', 'rb')
	try:
		beers = pickle.load(beersFile)
	except:
		beers = dict()
	beersFile.close()

	# load already processed breweries dictionary
	breweriesFile = open('breweries.pkl', 'rb')
	try:
		breweries = pickle.load(breweriesFile)
	except:
		breweries = dict()
	breweriesFile.close()
	
	# load already processed breweries dictionary
	breweryToBeersFile = open('breweryToBeers.pkl', 'rb')
	try:
		breweryToBeers = pickle.load(breweryToBeersFile)
	except:
		breweryToBeers = dict()
	breweryToBeersFile.close()

	lastLineNum = 0

	# keep track how many users have already been processed 
	try:
		with open('last_line.txt', 'rb') as lastFile:
			lastLineNum = int(lastFile.read())
	except:
		pass

	with open('userInfo_copy.csv', 'rb') as userNameFile:
		reader = csv.reader(userNameFile)
		for i, line in enumerate(reader):
			if i <= lastLineNum: continue
			userId = line[0]
			username = line[1]
			location = line[2]
			users[userId] = line[1:]
			userReviewCount = 4
			offsetTotal = 0
			users[userId].append({'ratings': []})

			print 'Processing ' + str(userId) + ': ' + username
			# each response returns at most 25 reviews. To get more user reviews, call again with an offset
			# get at most 100 reviews from the same user
			while (userReviewCount > 0):
				data = getUserReviewData(username, offsetTotal)
				offset = data['response']['beers']['count']
				offsetTotal += offset
				reviews = data['response']['beers']['items']
				for review in reviews:
					userRating = review['rating_score']
					if userRating > 0:
						beerInfo = review['beer']
						breweryInfo = review['brewery']

						# print 'user: ' + username + ', ' + 'beer_id: ' + str(beerInfo['bid']) + ': ' + str(userRating)
						# fill in beer information
						if beerInfo['bid'] not in beers:
							beer = {'name': unicode(beerInfo['beer_name']).encode("utf-8"), 'label': beerInfo['beer_label'],
							'abv': beerInfo['beer_abv'], 'ibu': beerInfo['beer_ibu'], 'style': unicode(beerInfo['beer_style']).encode("utf-8"),
							'description': unicode(beerInfo['beer_description']).encode("utf-8"), 'rating': beerInfo['rating_score'],
							'brewery': breweryInfo['brewery_id']}
							beers[beerInfo['bid']] = beer
						else:
							# the beer's overall rating may have changed in the time since it was stored
							beers[beerInfo['bid']]['rating'] = beerInfo['rating_score']

							# map breweery_id to a list of beers produced there
							if breweyInfo['brewery_id'] not in breweryToBeers:
								# store the current beer in a list of beers of the brewery
								breweryToBeers[breweryInfo['brewery_id']] = [beerInfo['bid']]
							else:
								# add current beer to brewery's list of beers
								breweryToBeers[breweryInfo['brewery_id']].append(beerInfo['bid'])

						# fill in brewery information
						if breweryInfo['brewery_id'] not in breweries:
							brewery = {'name': breweryInfo['brewery_name']).encode("utf-8"), 'label': breweryInfo['brewery_label'],
							'country': unicode(breweryInfo['country_name']).encode("utf-8"), 'location': unicode(breweryInfo['location']).encode("utf-8")}
							breweries[breweryInfo['brewery_id']] = brewery

						# add list of beer ratings to user
						users[userId][2]['ratings'].append({beerInfo['bid']: userRating})
				userReviewCount -= 1

				# store the dictionaries
				with open('users.pkl', 'wb') as usersFile:
					pickle.dump(users, usersFile)
				with open('beers.pkl', 'wb') as beersFile:
					pickle.dump(beers, beersFile)
				with open('breweries.pkl', 'wb') as breweriesFile:
					pickle.dump(breweries, breweriesFile)
				with open('breweryToBeers.pkl', 'wb') as breweryToBeersFile:
					pickle.dump(breweryToBeers, breweryToBeersFile)

				sleep(38)
				# if the offset is less than 25, then there are no more reviews to retrieve
				if offset < 25:
					break

			with open('last_line.txt', 'wb') as lastFile: lastFile.write(str(i))
			print str(userId) + ': ' + username + ', Processed: ' + str(len(users[userId][2]['ratings'])) + ' reviews'



main()