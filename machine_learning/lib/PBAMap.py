import urllib
import json
from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read('../apiConfig.ini')
# set the api setting values
baseUrl = "https://maps.googleapis.com/maps/api/geocode/json?"
apiKey = config.get('googleMaps', 'apiKey')
apiKey2 = config.get('googleMaps', 'apiKey2')


def getLatLong(address, calls):
    # Google Geocoding api only allows 2500 api calls a day
    # Update code to handle number of users and api keys
    url = ''
    if calls < 2500:
        url = baseUrl + "address=%s&sensor=false&key=%s" % (urllib.quote(address.replace(' ', '+')), apiKey)
    elif calls > 5000:
        url = baseUrl + "address=%s&sensor=false&key=%s" % (urllib.quote(address.replace(' ', '+')), apiKey2)
    if (url != ''):
        data = urllib.urlopen(url).read()
        info = json.loads(data).get("results")
        if info:
            location = info[0].get("geometry").get("location")
        else:
            location = ""
        return location
    else:
        return "apiLimit"
