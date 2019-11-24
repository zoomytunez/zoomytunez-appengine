import webapp2, urllib, logging, urllib2, json, cgi
from util import safeGet, pretty
from os import getenv

from api import spotify

SPOTIFY_REQUEST_PATH = "/auth/login/spotify"
SPOTIFY_CALLBACK_PATH = "/auth/spotify"
STRAVA_REQUEST_PATH = "/auth/login/strava"
STRAVA_CALLBACK_PATH = "/auth/strava"

SPOTIFY_OAUTH_URL = "https://accounts.spotify.com/authorize?"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
STRAVA_OAUTH_URL = "https://www.strava.com/oauth/authorize?"
STRAVA_TOKEN_URL = "https://www.strava.com/oauth/token"

SPOTIFY_SCOPE = "playlist-modify-private playlist-read-private"
STRAVA_SCOPE = "read,activity:read_all"


class SpotifyRequestHandler(webapp2.RequestHandler):
    def get(self):
        callback = self.request.host_url + SPOTIFY_CALLBACK_PATH
        params = {
            "response_type": "code",
            "client_id": getenv("SPOTIFY_ID"),
            "scope": SPOTIFY_SCOPE,
            "redirect_uri": callback
        }
        if 'force' in self.request.GET:
            params["show_dialog"] = "true"
        url = SPOTIFY_OAUTH_URL + urllib.urlencode(params)
        self.response.status = 302
        self.response.headers.add('Location', url)


class SpotifyCallbackHandler(webapp2.RequestHandler):
    def get(self):
        if 'error' in self.request.GET:
            self.response.status = 401
            self.response.write("<h1>Authorization unsuccessful</h1>")
            self.response.write("<p>An error occured: <code>")
            self.response.write(cgi.escape(self.request.GET['error']) + "</code>.</p>")
            return
        code = self.request.GET['code']
        callback = self.request.host_url + SPOTIFY_CALLBACK_PATH

        def errorHandler():
            self.response.status = 500
            self.response.write("An error occurred when getting the authorization token.")

        resp = safeGet(SPOTIFY_TOKEN_URL, {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": callback,
            "client_id": getenv("SPOTIFY_ID"),
            "client_secret": getenv("SPOTIFY_SECRET")
        }, error = errorHandler)
        if not resp: return

        data = json.load(resp)

        accessToken = data["access_token"]
        refreshToken = data["refresh_token"]

        # userId = spotify.

        # self.response.headers.add("Content-Type", "application/json")
        self.response.write("<h1>Authorization successful</h1>")
        self.response.write("<p>The following information was received:</p><pre>")
        self.response.write(cgi.escape(pretty(data)) + "</pre>")
        self.response.write('<script>history.replaceState({}, "", location.pathname)</script>')


class StravaRequestHandler(webapp2.RequestHandler):
    def get(self):
        callback = self.request.host_url + STRAVA_CALLBACK_PATH
        params = {
            "response_type": "code",
            "client_id": getenv("STRAVA_ID"),
            "scope": STRAVA_SCOPE,
            "redirect_uri": callback
        }
        if 'force' in self.request.GET:
            params['approval_prompt'] = "force"
        url = STRAVA_OAUTH_URL + urllib.urlencode(params)
        self.response.status = 302
        self.response.headers.add('Location', url)


class StravaCallbackHandler(webapp2.RequestHandler):
    def get(self):
        if 'error' in self.request.GET:
            self.response.status = 401
            self.response.write("<h1>Authorization unsuccessful</h1>")
            self.response.write("<p>An error occured: <code>")
            self.response.write(cgi.escape(self.request.GET['error']) + "</code>.</p>")
            return
        code = self.request.GET['code']
        scope = self.request.GET['scope']

        if scope != STRAVA_SCOPE:
            self.response.status = 401
            self.response.write("<h1>Authorization not granted</h1>")
            self.response.write("<p>Cannot read private activities. ")
            self.response.write('<a href="/auth/login/strava">(try again)</a></p>')
            self.response.write('<script>history.replaceState({}, "", location.pathname)</script>')
            return;

        def errorHandler():
            self.response.status = 500
            self.response.write("An error occurred when getting the authorization token.")

        resp = safeGet(STRAVA_TOKEN_URL, {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": getenv("STRAVA_ID"),
            "client_secret": getenv("STRAVA_SECRET")
        }, error=errorHandler)
        if not resp: return

        data = json.load(resp)

        # self.response.headers.add("Content-Type", "application/json")
        self.response.write("<h1>Authorization successful</h1>")
        self.response.write("<p>The following information was received:</p><pre>")
        self.response.write(cgi.escape(pretty(data)) + "</pre>")
        self.response.write('<script>history.replaceState({}, "", location.pathname)</script>')


route = webapp2.WSGIApplication([
    (SPOTIFY_REQUEST_PATH + "/?", SpotifyRequestHandler),
    (SPOTIFY_CALLBACK_PATH + "/?", SpotifyCallbackHandler),
    (STRAVA_REQUEST_PATH + "/?", StravaRequestHandler),
    (STRAVA_CALLBACK_PATH + "/?", StravaCallbackHandler),
], debug=True)