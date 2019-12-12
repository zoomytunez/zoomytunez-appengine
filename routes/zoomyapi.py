import webapp2, urllib, json
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

class BuildPlaylist(CORSRequestHandler):

    ALLOWED_METHODS = "POST"

    @checkOrigin
    @requiresAuth(user=True, spotify=True)
    def post(self, spotifyAPI):
        self.response.headers.add("Content-Type", "application/json")
        try:
            data = json.loads(self.request.body)
            artists = data["seeds"]["artists"]
            tracks = data["seeds"]["tracks"]
            genres = data["seeds"]["genres"]
            recommendationResults = spotifyAPI.getRecommendations(artists, tracks, genres)["tracks"]
            trackIDList = [track['id'] for track in recommendationResults]
            songOptions = spotifyAPI.getAudioFeatures(trackIDList)["audio_features"]
            curve = data["curve"]
            currentDuration = 0
            playlistSoFar = []
            while currentDuration < curve["duration"]:
                getScore = songFitScore(curve, currentDuration)
                sortedSongs = sorted(songOptions, key= getScore)
                bestFitSong = sortedSongs[random.randint(0,4)]
                songOptions = [song for song in songOptions if song != bestFitSong]
                playlistSoFar.append(bestFitSong)
                currentDuration += bestFitSong["duration_ms"]/1000
        except:
            self.response.status = 500
            self.response.write('{"error": true}')

def songFitScore(curve, currentDuration):
    def getScore(song):
        pass
    return getScore

class UserStatus(CORSRequestHandler):
    @checkOrigin
    @requiresAuth(user=True, spotify=True, strict=False)
    def get(self, user, spotifyAPI):
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
    def post(self, user=None):
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