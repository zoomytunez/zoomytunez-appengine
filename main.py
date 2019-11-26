import webapp2, os
from model import User

class MainHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.scheme == "http" and not ~self.request.host.find("localhost"):
            self.response.status = 301
            self.response.headers.add('Location', self.request.url.replace("http:", "https:", 1))
        self.response.write("<h1>ZoomyTunez</h1>")
        self.response.write('<br><a href="/auth/login/spotify">login with spotify</a> ')
        self.response.write('<a href="/auth/login/spotify?force=true">(force dialog)</a>')
        self.response.write('<br><a href="/auth/login/strava">login with strava</a> ')
        self.response.write('<a href="/auth/login/strava?force=true">(force dialog)</a>')
        self.response.write('<br><br><a href="/spotifytest">test spotify access</a>')
        if User.getForSession(self.request):
            self.response.write('<br>Logged in. <a href="/logout">logout</a>')
        else:
            self.response.write('<br>Not logged in.')
        self.response.write('<br><br><a href="test.html">static asset test</a>')

application = webapp2.WSGIApplication([('/', MainHandler)], debug=True)