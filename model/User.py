from google.appengine.ext import ndb

from util import cookie
import binascii, os
from api import SpotifyAPI

import logging

class User(ndb.Model):
    spotifyID = ndb.StringProperty(required=True)
    sessionCookie = ndb.StringProperty(indexed=False, required=True)
    spotifyAccessToken = ndb.StringProperty(indexed=False, required=True)
    spotifyRefreshToken = ndb.StringProperty(indexed=False, required=True)
    stravaAccessToken = ndb.StringProperty(indexed=False)
    stravaRefreshToken = ndb.StringProperty(indexed=False)
    savedPlaylists = ndb.StringProperty(indexed=False, repeated=True)
    height = ndb.IntegerProperty(indexed=False)

    def refreshSession(self):
        self.sessionCookie = binascii.hexlify(os.urandom(20)).decode()

    def clearSession(self):
        self.sessionCookie = None

    def getSpotifyAPI(self):
        return SpotifyAPI(self.spotifyAccessToken, self.spotifyRefreshToken, self)

    @classmethod
    def getBySpotifyID(cls, spotifyID):
        return User.query(User.spotifyID == spotifyID)

    @classmethod
    def getForSession(cls, req, getKey=False):
        userCookie = cookie.parse(req.cookies.get("user"))
        sessionCookie = cookie.parse(req.cookies.get("session"))
        if not userCookie or not sessionCookie:
            return None
        try:
            key = ndb.Key(urlsafe=userCookie)
            user = key.get()
            if user.sessionCookie and user.sessionCookie == sessionCookie:
                if getKey:
                    return key
                else:
                    return user
            return None
        except:
            return None

    @classmethod
    def getSpotifyForSession(cls, req):
        user = User.getForSession(req)
        return (user.getSpotifyAPI() if user else None)
