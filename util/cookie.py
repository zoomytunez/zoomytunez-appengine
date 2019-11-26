import base64, Cookie

def set(response, name, value, domain=None, path="/", expires=None):
    value = base64.b64encode(value)
    cookie = Cookie.BaseCookie()
    cookie[name] = value
    cookie[name]["path"] = path
    if domain: cookie[name]["domain"] = domain
    if expires:
        cookie[name]["expires"] = email.utils.formatdate(
            expires, localtime=False, usegmt=True)
    response.headers.add("Set-Cookie", cookie.output()[12:])


def parse(value):
    if not value: return None
    try:
        return base64.b64decode(value).strip()
    except:
        return None