import webapp2, cgi
from util import cookie, pretty
from model import User
from api import spotify

import logging

class SpotifyTestHandler(webapp2.RequestHandler):
    def get(self):
        user = User.getForSession(self.request)
        if not user:
            self.response.write("<h1>Not logged in or session expired</h1>")
            self.response.write('<a href="/auth/login/spotify">login</a>')
            return
        self.response.write("<h1>Your information:</h1>")
        data = spotify.getUserInformation(user.spotifyAccessToken, user.spotifyRefreshToken)
        self.response.write("<pre>")
        self.response.write(cgi.escape(pretty(data)))
        self.response.write('</pre>')
        self.response.write('<a href="/">home</a> <a href="/logout">logout</a> ')

route = webapp2.WSGIApplication([
    ("/spotifytest", SpotifyTestHandler)
])