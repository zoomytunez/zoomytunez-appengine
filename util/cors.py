import webapp2
from model import User

def requiresAuth(spotify=False, strava=False):
    def decorator(func):
        def wrapper(self):
            kwargs = {}
            session = None
            if spotify or strava:
                user = User.getForSession(self.request)
            if spotify:
                try:
                    spotifyAPI = user.getSpotifyAPI()
                    if not spotifyAPI: raise Error()
                except:
                    self.response.status = 401
                    self.response.write("Unauthorized")
                    return
                kwargs["spotifyAPI"] = spotifyAPI
            if strava:
                # stravaAPI = user.getStravaAPI()
                # if not stravaAPI:
                    # self.response.status = 401
                    # self.response.write("Unauthorized")
                    # return
                # kwargs["stravaAPI"] = stravaAPI
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
    def wrapper(self):
        if "Origin" in self.request.headers:
            origin = self.request.headers["Origin"]
            if not _originTest(origin):
                self.response.status = 403
            self.response.headers.add("Access-Control-Allow-Origin", origin)
            self.response.headers.add("Vary", "Origin")
            self.response.headers.add("Access-Control-Allow-Credentials", "true")
            if func.__name__ == "options" and self.CORS_METHODS:
                self.response.headers.add("Access-Control-Allow-Methods", self.CORS_METHODS)
        func(self)
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