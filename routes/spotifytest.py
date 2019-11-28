import webapp2, cgi
from util import cookie, pretty
from model import User

import logging

class SpotifyInfo(webapp2.RequestHandler):
    def get(self):
        # user = User.getForSession(self.request)
        # userSpotify = user.getSpotifyAPI()

        userSpotify = User.getSpotifyForSession(self.request)

        if not userSpotify:
            self.response.write("<h1>Not logged in or session expired</h1>")
            self.response.write('<a href="/auth/login/spotify">login</a>')
            return
        self.response.write("<h1>Your information:</h1>")
        data = userSpotify.getUserInformation()
        self.response.write("<pre>")
        self.response.write(cgi.escape(pretty(data)))
        self.response.write('</pre>')
        self.response.write('<a href="/">home</a> <a href="/logout">logout</a> ')


class SpotifyPlaylists(webapp2.RequestHandler):
    def get(self):
        # user = User.getForSession(self.request)
        # userSpotify = user.getSpotifyAPI()

        userSpotify = User.getSpotifyForSession(self.request)

        if not userSpotify:
            self.response.write("<h1>Not logged in or session expired</h1>")
            self.response.write('<a href="/auth/login/spotify">login</a>')
            return
        self.response.write("<h1>Your playlists:</h1>")
        data = userSpotify.getPlaylists()

        for playlist in data["items"]:
            self.response.write("<hr>")
            self.response.write('<img src="%s" width="64" height="64">' % playlist["images"][0]["url"])
            self.response.write(cgi.escape(playlist["name"]))

        self.response.write("<pre>")
        self.response.write(cgi.escape(pretty(data)))
        self.response.write('</pre>')
        self.response.write('<a href="/">home</a> <a href="/logout">logout</a> ')

route = webapp2.WSGIApplication([
    ("/spotifytest/info", SpotifyInfo),
    ("/spotifytest/playlists", SpotifyPlaylists)
])