import webapp2
from util import cookie, pretty
from model import User
from api import spotify

class SpotifyTestHandler(webapp2.RequestHandler):
    def get(self):

        sessionid = cookie.parse(self.request.cookies.get("session"))
        userKeyString = cookie.parse(self.request.cookies.get("user"))

        try:
            if not sessionid or not userKeyString:
                raise Error()
            user = User.getByKeyString(userKeyString)
            data = spotify.getUserInformation(user.spotifyAccessToken, user.spotifyRefreshToken)
            self.response.write(pretty(data))
        except:
            self.response.write("Not logged in.")

route = webapp2.WSGIApplication([
    ("/spotifytest/?", SpotifyTestHandler)
])