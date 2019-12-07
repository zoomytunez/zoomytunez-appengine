import urllib2, logging, urllib
import json as jsonModule

def _noop(*args):
    pass

def safeGet(url, data=None, error=_noop, auth=None, bearer=None, json=False):
    req = urllib2.Request(url)
    if bearer:
        auth = "Bearer " + bearer
    if auth:
        req.add_header("Authorization", auth)
    try:
        if data:
            if json:
                req.add_header("Content-Type", "application/json")
                return urllib2.urlopen(req, jsonModule.dumps(data))
            else:
                return urllib2.urlopen(req, urllib.urlencode(data))
        else:
            return urllib2.urlopen(req)
    except urllib2.HTTPError as e:
        logging.error("The server couldn't fulfill the request.")
        logging.error("Error code: " + str(e.code))
        if error: return error(e)
        return None
    except urllib2.URLError as e:
        logging.error("We failed to reach a server")
        logging.error("Reason: " + str(e.reason))
        if error: return error(e)
        return None