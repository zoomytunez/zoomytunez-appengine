import urllib2, logging, urllib

def safeGet(url, data=None):
    try:
        return urllib2.urlopen(url, urllib.urlencode(data))
    except urllib2.HTTPError as e:
        logging.error("The server couldn't fulfill the request.")
        logging.error("Error code: " + str(e.code))
        return e
    except urllib2.URLError as e:
        logging.error("We failed to reach a server")
        logging.error("Reason: " + str(e.reason))
        return None