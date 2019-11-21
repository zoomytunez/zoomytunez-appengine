import webapp2, os

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("Hello, world!")
        self.response.write("<br>Secret variable: ")
        self.response.write(os.getenv("SECRET"))
        self.response.write('<br><a href="test.html">static asset test</a>')
        self.response.write('<br><a href="/auth/login/spotify">login with spotify</a> ')
        self.response.write('<a href="/auth/login/spotify?force=true">(force dialog)</a>')
        self.response.write('<br><a href="/auth/login/strava">login with strava</a> ')
        self.response.write('<a href="/auth/login/strava?force=true">(force dialog)</a>')

application = webapp2.WSGIApplication([('/', MainHandler)], debug=True)