from util import safeGet, pretty

def getNewAcessToken(refreshToken):


def getUserInformation(accessToken, refreshToken):

    def errorHandler():


    safeGet("spotify/whatever", error=errorHandler)
