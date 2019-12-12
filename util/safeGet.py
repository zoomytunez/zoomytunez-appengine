import urllib2, logging, urllib
import json as jsonModule

def _noop(*args):
    pass

# https://stackoverflow.com/a/31839324
class MethodRequest(urllib2.Request):
    def __init__(self, *args, **kwargs):
        if 'method' in kwargs:
            self._method = kwargs['method']
            del kwargs['method']
        else:
            self._method = None
        return urllib2.Request.__init__(self, *args, **kwargs)

    def get_method(self, *args, **kwargs):
        if self._method is not None:
            return self._method
        return urllib2.Request.get_method(self, *args, **kwargs)

def safeGet(url, data=None, error=_noop, auth=None, bearer=None, json=False, method="GET"):
    if method == "GET" and data:
        method = "POST"
    req = MethodRequest(url, method=method)
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
        logging.error("!!Error fetching " + url)
        logging.error("Data: " + jsonModule.dumps(data))
        logging.error("The server couldn't fulfill the request.")
        logging.error("Error code: " + str(e.code))
        if error: return error(e)
        return None
    except urllib2.URLError as e:
        logging.error("We failed to reach a server")
        logging.error("Reason: " + str(e.reason))
        if error: return error(e)
        return None