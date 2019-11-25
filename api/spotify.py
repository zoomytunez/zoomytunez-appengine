from util import safeGet, pretty
import json, base64
from os import getenv

URL = "https://api.spotify.com/v1/"


def getAccessToken(code, callback, error=None):
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
    return data

def refreshAccessToken(refreshToken, error=None):
    b64string = base64.b64encode("%s:%s" % (getenv('SPOTIFY_ID'), getenv('SPOTIFY_SECRET')))
    auth = "Basic " + b64string
    res = safeGet("https://accounts.spotify.com/api/token", data={
        "grant_type": "refresh_token",
        "refresh_token": refreshToken
    }, auth = auth, error = error)
    if not res: return None
    data = json.load(res)
    return data["access_token"]

def getUserInformation(accessToken, refreshToken, error=None):
    res = safeGet(URL + "me", auth = ("Bearer %s" % accessToken),  error = error)
    if not res: return None
    data = json.load(res)
    return data
