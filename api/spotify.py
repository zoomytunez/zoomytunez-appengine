from util import safeGet, pretty
import json, base64, urllib
from os import getenv

URL = "https://api.spotify.com/v1/"

def refreshAndRetry(self, cb):
    def errorHandler(e):
        attempt = False # self.refreshAccessToken(error=None)
        if attempt:
            return cb()
        else:
            return None
    return errorHandler


class SpotifyAPI():
    def __init__(self, accessToken=None, refreshToken=None, dbUser=None):
        self.accessToken = accessToken
        self.refreshToken = refreshToken
        self.dbUser = dbUser

    def getUserInformation(self):
        error = refreshAndRetry(self, lambda: self.getUserInformation())
        res = safeGet(URL + "me", auth = ("Bearer %s" % self.accessToken), error = error)
        if not res: return None
        data = json.load(res)
        return data

    def getPlaylists(self):
        error = refreshAndRetry(self, lambda: self.getPlaylists())
        res = safeGet(URL + "me/playlists", auth = ("Bearer %s" % self.accessToken), error = error)
        if not res: return None
        data = json.load(res)
        return data

    def search(self, query, limit=20, offset=0, parse=True):
        searchType = "artist,track"
        params = {
            "q": query,
            "type": searchType,
            "limit": limit,
            "offset": offset
        }
        error = refreshAndRetry(self, lambda: self.search())
        res = safeGet(URL + "search?" + urllib.urlencode(params), auth = ("Bearer %s" % self.accessToken), error = error)
        if not res: return None
        if parse:
            return json.load(res)
        else:
            return res.read()

    def getGenres(self, parse=True):
        error = refreshAndRetry(self, lambda: self.getGenres())
        res = safeGet(URL + "recommendations/available-genre-seeds", auth = ("Bearer %s" % self.accessToken), error = error)
        if not res: return None
        if parse:
            return json.load(res)
        else:
            return res.read()

    def refreshAccessToken(self, error=None):
        """Gets a new refresh token for this user; returns true if successful"""
        b64string = base64.b64encode("%s:%s" % (getenv('SPOTIFY_ID'), getenv('SPOTIFY_SECRET')))
        auth = "Basic " + b64string
        res = safeGet("https://accounts.spotify.com/api/token", data={
            "grant_type": "refresh_token",
            "refresh_token": self.refreshToken
        }, auth = auth, error = error)
        if not res: return None
        logging.warn(res)
        data = json.load(res)
        self.accessToken = data["access_token"]
        if self.dbUser:
            self.dbUser.spotifyAccessToken = self.accessToken
            self.dbUser.put()
        return True

    @classmethod
    def getFromCode(cls, code, callback, error=None):
        b64string = base64.b64encode("%s:%s" % (getenv('SPOTIFY_ID'), getenv('SPOTIFY_SECRET')))
        auth = "Basic " + b64string
        res = safeGet("https://accounts.spotify.com/api/token", {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": callback,
            "client_id": getenv("SPOTIFY_ID"),
            "client_secret": getenv("SPOTIFY_SECRET")
        }, auth = auth, error = error)
        if not res: return None
        data = json.load(res)
        return SpotifyAPI(accessToken=data["access_token"], refreshToken=data["refresh_token"])

