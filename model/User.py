from google.appengine.ext import ndb

import binascii, os

class User(ndb.Model):
    spotifyID = ndb.StringProperty(required=True)
    sessionCookie = ndb.StringProperty(indexed=False, required=True)
    spotifyAccessToken = ndb.StringProperty(indexed=False, required=True)
    spotifyRefreshToken = ndb.StringProperty(indexed=False, required=True)
    stravaAccessToken = ndb.StringProperty(indexed=False)
    stravaRefreshToken = ndb.StringProperty(indexed=False)
    savedPlaylists = ndb.StringProperty(indexed=False, repeated=True)

    def refreshSession(self):
        self.sessionCookie = binascii.hexlify(os.urandom(20)).decode()

    @classmethod
    def getBySpotifyID(cls, spotifyID):
        return User.query(User.spotifyID == spotifyID)

    @classmethod
    def getByKeyString(cls, keyString):
        key = ndb.Key(urlsafe=keyString)
        return key.get()