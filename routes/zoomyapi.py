import webapp2, urllib, json
from model import User
from util.cors import requiresAuth, checkOrigin, CORSRequestHandle

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

class SpotifyRecommendations(CORSRequestHandler):
    @checkOrigin
    @requiresAuth(spotify=True)
    #not sure how to get the list of seeds from user
    def get(self, spotifyAPI):
        recommendationResults = spotifyAPI.getRecommendations(seedList)["tracks"]
        trackIDList = []
        for track in recommendationResults:
            trackIDList.append(track["id"])
        return getAudioFeatures(trackIDList)

class UserStatus(CORSRequestHandler):
    @checkOrigin
    @requiresAuth(user=True, spotify=True, strict=False)
    def get(self, user=None, spotifyAPI=None):
        self.response.headers.add("Content-Type", "application/json")
        if user:
            info = spotifyAPI.getUserInformation()
            data = {}
            data["user"] = info["display_name"]
            data["photo"] = info["images"][0]["url"] if info["images"] else None
            data["height"] = user.height
            data["playlists"] = user.savedPlaylists
            self.response.write(json.dumps(data))
        else:
            self.response.write('{"user":null}')

class SetUserHeight(CORSRequestHandler):

    ALLOWED_METHODS = "POST"

    @checkOrigin
    @requiresAuth(user=True)
    def post(self, user):
        self.response.headers.add("Content-Type", "application/json")
        try:
            height = int(self.request.body)
            if height < 0 or height > 5000: raise Error()
            user.height = height
            user.put()
            data = {"height": height}
            self.response.write(json.dumps(data))
        except:
            self.response.status = 500
            self.response.write('{"error": true}')

route = webapp2.WSGIApplication([
    ("/api/search", SpotifySearch),
    ("/api/list-genres", SpotifyGenres),
    ("/api/user", UserStatus),
    ("/api/user/height", SetUserHeight),
])