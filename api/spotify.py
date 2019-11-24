from util import safeGet, pretty
import json, base64
from os import getenv

URL = "https://api.spotify.com/v1/"

def getNewAcessToken(refreshToken):
    b64string = base64.b64encode("%s:%s" % (getenv('SPOTIFY_ID'), getenv('SPOTIFY_SECRET')))
    auth = "Basic " + b64string
    res = safeGet("https://accounts.spotify.com/api/token", data={
        "grant_type": "refresh_token",
        "refresh_token": refreshToken
    }, auth= auth)
    data = json.load(res)
    return data["access_token"]

def getUserInformation(accessToken, refreshToken):
    def errorHandler():
        pass
    safeGet(URL + "me", auth= authToken,  error=errorHandler)
