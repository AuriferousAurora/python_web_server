# Standard library imports
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

# Third-party imports
import requests
import uuid

# Local imports
from constants import BASE_URL, CLIENT_ID

def build_auth_url(client_id, response_type, redirect_uri, port, duration = 'temporary', scope = 'read'):
    state = str(uuid.uuid4())
    url = BASE_URL + 'authorize?client_id=' + client_id + '&response_type=' + response_type + '&state=' + state + '&redirect_uri=' + redirect_uri + ':' + port + '&duration=' + duration + '&scope=' + scope

    return url

def reddit_auth():
    url = build_auth_url(CLIENT_ID, 'code', 'http://localhost', '4242')
    response = requests.get(url)

    print(response.status_code)
    print(response.headers)
    print(response.text)
    print(response.json)

    if response.ok:
        return response
    else:
        return None