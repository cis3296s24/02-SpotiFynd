from requests import get
from re import search
from json import loads

def access_token():
    response = get("https://open.spotify.com/search")
    match = search('<script id="session" data-testid="session" type="application/json">({.*})</script>', response.text)
    json_data = loads(match.group(1))
    access_token = json_data.get('accessToken')
    return access_token

