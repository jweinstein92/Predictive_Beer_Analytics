import urllib
import json

baseUrl = "https://maps.googleapis.com/maps/api/geocode/json?"
apiKey = "AIzaSyDq9nem-_iBZNjTZwBFZP5MZ5hRN9D8rUU"
apiKey2 = "AIzaSyDaKr6isl5KfjvWnFngsX9NVADsPojUlyg"


def getLatLong(address, calls):
    if calls < 2400:
        url = baseUrl + "address=%s&sensor=false&key=%s" % (urllib.quote(address.replace(' ', '+')), apiKey2)
    else:
        url = baseUrl + "address=%s&sensor=false&key=%s" % (urllib.quote(address.replace(' ', '+')), apiKey)
    data = urllib.urlopen(url).read()
    info = json.loads(data).get("results")
    if info:
        location = info[0].get("geometry").get("location")
    else:
        location = ""
    return location
