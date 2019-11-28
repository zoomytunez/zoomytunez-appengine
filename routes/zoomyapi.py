import webapp2, urllib
from model import User

class SpotifySearch(webapp2.RequestHandler):
    def get(self):
        params = self.request.GET
        if "q" not in params:
            self.response.status = 400
            return
        spotifyAPI = User.getSpotifyForSession(self.request)
        if not spotifyAPI:
            self.response.status = 401
            return
        limit = params["limit"] if "limit" in params else 20
        offset = params["offset"] if "offset" in params else 0
        searchResults = spotifyAPI.search(
            params["q"],
            limit = limit,
            offset = offset,
            parse = False
        )
        self.response.headers.add("Content-Type", "application/json")
        self.response.write(searchResults)

route = webapp2.WSGIApplication([
    ("/api/search", SpotifySearch),
    ("/api/list-genres", SpotifyGenres)
])

class SpotifyGenres(webapp2.RequestHandler):
    def get(self):
        params = self.request.GET
        if "q" not in params:
            self.response.status = 400
            return
        spotifyAPI = User.getSpotifyForSession(self.request)
        if not spotifyAPI:
            self.response.status = 401
            return
        searchResults = spotifyAPI.getGenres()
        self.response.headers.add("Content-Type", "application/json")
        self.response.write(searchResults)
