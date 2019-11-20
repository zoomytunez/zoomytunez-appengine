import webapp2, urllib, logging, urllib2, json
from util import safeGet, pretty
from os import getenv

SPOTIFY_REQUEST_PATH = "/auth/login/spotify"
SPOTIFY_CALLBACK_PATH = "/auth/spotify"
STRAVA_REQUEST_PATH = "/auth/login/strava"
STRAVA_CALLBACK_PATH = "/auth/strava"

SPOTIFY_OAUTH_URL = "https://accounts.spotify.com/authorize?"

class SpotifyRequestHandler(webapp2.RequestHandler):
    def get(self):
        scopes = "playlist-modify-private playlist-read-private"
        callback = self.request.host_url + SPOTIFY_CALLBACK_PATH
        params = {
            "response_type": "code",
            "client_id": getenv("SPOTIFY_ID"),
            "scope": scopes,
            "redirect_uri": callback
        }
        if ('force' in self.request.GET):
            params["show_dialog"] = "true"
        url = SPOTIFY_OAUTH_URL + urllib.urlencode(params)
        self.response.status = 302
        self.response.headers.add('Location', url)

class SpotifyCallbackHandler(webapp2.RequestHandler):
    def get(self):
        if ('error' in self.request.GET):
            self.response.status = 401
            self.response.write("error: " + self.request.GET['error'])
            return
        code = self.request.GET['code']
        callback = self.request.host_url + SPOTIFY_CALLBACK_PATH

        resp = safeGet.safeGet("https://accounts.spotify.com/api/token", {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": callback,
            "client_id": getenv("SPOTIFY_ID"),
            "client_secret": getenv("SPOTIFY_SECRET")
        })

        data = json.load(resp)

        self.response.headers.add("Content-Type", "application/json")
        self.response.write(pretty.pretty(data))

class StravaRequestHandler(webapp2.RequestHandler):
    def get(self):
        pass

class StravaCallbackHandler(webapp2.RequestHandler):
    def get(self):
        pass


route = webapp2.WSGIApplication([
    (SPOTIFY_REQUEST_PATH, SpotifyRequestHandler),
    (SPOTIFY_CALLBACK_PATH, SpotifyCallbackHandler),


], debug=True)