import webapp2, urllib, json, random, logging
from model import User
from util.cors import requiresAuth, checkOrigin, CORSRequestHandler

class SpotifySearch(CORSRequestHandler):
    @checkOrigin
    @requiresAuth(spotify=True)
    def get(self, spotifyAPI=None):
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
    def get(self, spotifyAPI=None):
        searchResults = spotifyAPI.getGenres(parse=False)
        self.response.headers.add("Content-Type", "application/json")
        self.response.write(searchResults)

class BuildPlaylist(CORSRequestHandler):

    ALLOWED_METHODS = "POST"

    @checkOrigin
    @requiresAuth(user=True, spotify=True)
    def post(self, user=None, spotifyAPI=None):
        self.response.headers.add("Content-Type", "application/json")
        # try:
        data = json.loads(self.request.body)
        artists = ",".join(data["seeds"]["artists"])
        tracks = ",".join(data["seeds"]["tracks"])
        genres = ",".join(data["seeds"]["genres"])
        minbpm = 500
        maxbpm = 0
        curve = data["curve"]
        for point in curve["points"]:
            minbpm = min(minbpm, point["bpm"])
            maxbpm = max(maxbpm, point["bpm"])

        # get recommendations from spotify
        recommendationResults = spotifyAPI.getRecommendations(
            artists, tracks, genres,
            bpmrange=(round(minbpm - 10), round(maxbpm + 10))
        )["tracks"]

        # create id -> track lookup table for later
        trackLookup = {}
        for track in recommendationResults:
            trackLookup[track['id']] = track

        # get audio features for all tracks from spotify
        trackIDList = [track['id'] for track in recommendationResults]
        songOptions = spotifyAPI.getAudioFeatures(trackIDList)["audio_features"]

        if len(songOptions) < 50:
            self.response.write('{"error": "SMALL_RECOMMENDATION_POOL"}')
            return

        # build the playlist!
        currentDuration = 0
        playlistSoFar = []
        while currentDuration < curve["duration"]:
            getScore = songFitScore(curve, currentDuration)
            sortedSongs = sorted(songOptions, key=getScore)
            bestFitSong = sortedSongs[random.randint(0,4)]
            songOptions = [song for song in songOptions if song != bestFitSong]
            playlistSoFar.append(bestFitSong)
            currentDuration += bestFitSong["duration_ms"]/1000

        # make it a playlist!
        username = user.spotifyID
        playlist = spotifyAPI.createPlaylist(username, "ZoomyTunez Run")
        playlistID = playlist["id"]

        spotifyAPI.addTracks([track["uri"] for track in playlistSoFar], playlistID)

        playlistData = [trackLookup[track["id"]] for track in playlistSoFar]
        for i in range(len(playlistData)):
            playlistData[i]["bpm"] = playlistSoFar[i]["tempo"]

        responseData = {
            "uri": playlist["uri"],
            "tracks": playlistData
        }

        self.response.write(json.dumps(responseData))

        # except Exception as e:
        #     print(e)
        #     self.response.status = 500
        #     self.response.write('{"error": true}')

def songFitScore(curve, currentDuration):
    def getScore(song):
        songStart = currentDuration
        songEnd = currentDuration + song["duration_ms"]/1000

        relevantSegments = [(
            (segment, min(segment["end"], songEnd) - max(segment["start"], songStart))
        ) for segment in curve["points"] if not (
            segment["end"] <= songStart or songEnd <= segment["start"]
        )]

        score = 0
        for (segment, overlap) in relevantSegments:
            score += abs(segment["bpm"] - song["tempo"]) * overlap
        return score
    return getScore

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
    ("/api/playlist/build", BuildPlaylist),
])