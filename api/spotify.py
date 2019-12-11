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

    def getUserInformation(self, parse=True):
        error = refreshAndRetry(self, lambda: self.getUserInformation())
        res = safeGet(URL + "me", bearer = self.accessToken, error = error)
        if not res: return None
        if parse:
            return json.load(res)
        else:
            return res.read()

    def getPlaylists(self, parse=True):
        error = refreshAndRetry(self, lambda: self.getPlaylists())
        res = safeGet(URL + "me/playlists", bearer = self.accessToken, error = error)
        if not res: return None
        if parse:
            return json.load(res)
        else:
            return res.read()

    #jordan pls check over this
    def getRecommendations(self, artists, tracks, genres, parse=True):
        params = {
            "seed_artists": artists,
            "seed_tracks": tracks,
            "seed_genres": genres,
            "limit": 100
        }
        error = refreshAndRetry(self, lambda: self.getRecommendations())
        res = safeGet(URL + "recommendations?" + urllib.urlencode(params), bearer = self.accessToken, error = error)
        if not res: return None
        if parse:
            return json.load(res)
        else:
            return res.read()

    def getPlaylistTracks(self, playlistID, parse=True):
        error = refreshAndRetry(self, lambda: self.getPlaylistTracks(playlistID))
        res = safeGet(URL + "playlists/" + playlistID + "/tracks", bearer = self.accessToken, error = error)
        if not res: return None
        if parse:
            return json.load(res)
        else:
            return res.read()

    #trackIDS should be a list of ids
    def getAudioFeatures(self, trackIDs, parse=True):
        error = refreshAndRetry(self, lambda: self.getAudioFeatures())
        res = safeGet(URL + "audio-features/?" + urllib.urlencode(trackIDs), bearer = self.accessToken, error = error)
        if not res: return None
        if parse:
            return json.load(res)
        else:
            return res.read()

    def getAudioAnalysis(self, trackID, parse=True):
        error = refreshAndRetry(self, lambda: self.getAudioAnalysis())
        res = safeGet(URL + "audio-analysis/" + trackID, bearer = self.accessToken, error = error)
        if not res: return None
        if parse:
            return json.load(res)
        else:
            return res.read()

    def createPlaylist(self, username, playlistName, parse=True):
        error = refreshAndRetry(self, lambda: self.createPlaylist())
        playlistData = {"name": playlistName, "public": False, "description": "A running playlist made just for you by ZoomyTunez"}
        res = safeGet(URL + "users/" + username + "/playlists", bearer = self.accessToken, data=playlistData, error = error, json=True)
        if not res: return None
        if parse:
            return json.load(res)
        else:
            return res.read()

    def search(self, query, limit=20, offset=0, parse=True):
        searchType = "artist,track"
        params = {
            "q": query,
            "type": searchType,
            "limit": limit,
            "offset": offset
        }
        error = refreshAndRetry(self, lambda: self.search())
        res = safeGet(URL + "search?" + urllib.urlencode(params), bearer = self.accessToken, error = error)
        if not res: return None
        if parse:
            return json.load(res)
        else:
            return res.read()

    def getGenres(self, parse=True):
        error = refreshAndRetry(self, lambda: self.getGenres())
        res = safeGet(URL + "recommendations/available-genre-seeds", bearer = self.accessToken, error = error)
        if not res: return None
        if parse:
            return json.load(res)
        else:
            return res.read()

    def addTracks(self, uris, playlistID, parse=True):
        error = refreshAndRetry(self, lambda: self.addTracks())
        res = safeGet(URL + "playlists/" + playlistID + "/tracks",
                      data=uris, json=True,
                      bearer=self.accessToken, error=error)
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

