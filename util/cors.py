import webapp2
from model import User

def requiresAuth(spotify=False, strava=False, user=False, strict=True):
    def decorator(func):
        def wrapper(self):
            kwargs = {}
            session = None
            dbUser = User.getForSession(self.request)
            if strict and not dbUser:
                self.response.status = 401
                self.response.write("Unauthorized")
                return
            if user:
                kwargs["user"] = dbUser
            if dbUser and spotify:
                spotifyAPI = dbUser.getSpotifyAPI()
                if strict and not spotifyAPI:
                    self.response.status = 401
                    self.response.write("Unauthorized")
                    return
                kwargs["spotifyAPI"] = spotifyAPI
            if dbUser and strava:
                pass # need to implement strava api
            func(self, **kwargs)
        return wrapper
    return decorator


ACCEPTABLE_REFERERS = ["localhost", "zoomy-tunez-fb.web.app", "zoomy-tunez-fb.firebaseapp.com", "zoomytunez.appspot.com"]

def _originTest(origin):
    parts = origin.split(":")
    if parts[0] == "http" and parts[1] != "//localhost":
        return False # don't allow http requests if not local
    if parts[1][2:] in ACCEPTABLE_REFERERS:
        return True
    return False

def checkOrigin(func):
    def wrapper(self, *args, **kwargs):
        if "Origin" in self.request.headers:
            origin = self.request.headers["Origin"]
            if not _originTest(origin):
                self.response.status = 403
                self.response.write("Not allowed")
                return
            self.response.headers.add("Access-Control-Allow-Origin", origin)
            self.response.headers.add("Access-Control-Allow-Headers", "Content-Type")
            self.response.headers.add("Vary", "Origin")
            self.response.headers.add("Access-Control-Allow-Credentials", "true")
            if func.__name__ == "options" and self.CORS_METHODS:
                self.response.headers.add("Access-Control-Allow-Methods", self.CORS_METHODS)
        func(self, *args, **kwargs)
    return wrapper

class CORSRequestHandler(webapp2.RequestHandler):

    CORS_METHODS = "GET"

    @checkOrigin
    def options(self):
        pass

# Usage:
#
# class Handler(CORSRequestHandler):
#
#     CORS_METHODS = "GET, POST"
#
#     @checkOrigin
#     @requiresAuth(spotify=True)
#     def get(self, spotifyAPI):
#         ...
#
#     @checkOrigin
#     @requiresAuth(spotify=True)
#     def post(self, spotifyAPI):
#         ...