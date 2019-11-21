import urllib2, logging, urllib

def _noop():
    pass

def safeGet(url, data=None, error=_noop):
    try:
        return urllib2.urlopen(url, urllib.urlencode(data))
    except urllib2.HTTPError as e:
        logging.error("The server couldn't fulfill the request.")
        logging.error("Error code: " + str(e.code))
        error(e)
        return None
    except urllib2.URLError as e:
        logging.error("We failed to reach a server")
        logging.error("Reason: " + str(e.reason))
        error(e)
        return None