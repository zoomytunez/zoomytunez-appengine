import webapp2, os

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("Hello, world!")
        self.response.write("<br>Secret variable: ")
        self.response.write(os.getenv("SECRET"))
        self.response.write('<br><a href="test.html">static</a>')

application = webapp2.WSGIApplication([('/', MainHandler)], debug=True)