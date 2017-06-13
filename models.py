from google.appengine.ext import ndb


class Review(ndb.Model):
    beerName = ndb.StringProperty(required=True)
    style = ndb.StringProperty(default=None)
    brewery = ndb.StringProperty(default=None)
    rating = ndb.StringProperty(default=None)
    userId = ndb.StringProperty(required=True)
