from google.appengine.ext import ndb

from util import cookie
import binascii, os

import logging

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

    def clearSession(self):
        self.sessionCookie = None

    @classmethod
    def getBySpotifyID(cls, spotifyID):
        return User.query(User.spotifyID == spotifyID)

    @classmethod
    def getForSession(cls, req):
        userCookie = cookie.parse(req.cookies.get("user"))
        sessionCookie = cookie.parse(req.cookies.get("session"))
        if not userCookie or not sessionCookie:
            return None
        try:
            key = ndb.Key(urlsafe=userCookie)
            user = key.get()
            if user.sessionCookie and user.sessionCookie == sessionCookie:
                return user
            return None
        except:
            return None