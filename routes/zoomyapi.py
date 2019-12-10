import webapp2, urllib
from model import User
from util.cors import requiresAuth, checkOrigin, CORSRequestHandler

class SpotifySearch(CORSRequestHandler):
    @checkOrigin
    @requiresAuth(spotify=True)
    def get(self, spotifyAPI):
        params = self.request.GET
        if "q" not in params:
            self.response.status = 400
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

class SpotifyGenres(CORSRequestHandler):
    @checkOrigin
    @requiresAuth(spotify=True)
    def get(self, spotifyAPI):
        searchResults = spotifyAPI.getGenres(parse=False)
        self.response.headers.add("Content-Type", "application/json")
        self.response.write(searchResults)

class UserStatus(CORSRequestHandler):
    @checkOrigin
    @requiresAuth(spotify=True)
    def get(self, spotifyAPI):
        info = spotifyAPI.getUserInformation()

        self.response.headers.add("Content-Type", "application/json")
        self.response.write('{"status":"ok"}')

route = webapp2.WSGIApplication([
    ("/api/search", SpotifySearch),
    ("/api/list-genres", SpotifyGenres),
    ("/api/user", UserStatus)
])