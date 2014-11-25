class dataPoint:
    def __init__(self, attribs):
        self.lat = attribs['lat']
        self.lng = attribs['lng']
        self.abv = attribs['abv']
        self.rating = attribs['rating']


class dataPoints:
    def __init__(self, points):
        self.points = points
