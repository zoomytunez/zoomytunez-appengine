import base64, Cookie, email

def set(response, name, value, domain=None, path="/", expires=None, secure=True):
    value = base64.b64encode(value)
    cookie = Cookie.BaseCookie()
    cookie[name] = value
    cookie[name]["path"] = path
    cookie[name]["httponly"] = True
    if secure:
        cookie[name]["Secure"] = True
    if domain: cookie[name]["domain"] = domain
    if expires:
        cookie[name]["expires"] = email.utils.formatdate(
            expires, localtime=False, usegmt=True)
    cookieOutput = cookie.output()[12:]
    # going same-origin for now - might come back to this eventually
    # if secure:
        # cookieOutput = cookieOutput + "; SameSite=None"
    response.headers.add("Set-Cookie", cookieOutput)

def clear(response, name, path="/"):
    cookie = Cookie.BaseCookie()
    cookie[name] = ""
    cookie[name]["path"] = path
    cookie[name]["expires"] = "Thu, 01 Jan 1970 00:00:00 GMT"
    response.headers.add("Set-Cookie", cookie.output()[12:])

def parse(value):
    if not value: return None
    try:
        return base64.b64decode(value).strip()
    except:
        return None