from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from django.conf import settings

def get_token(client_id: str, client_secret: str, verify: str = True):
    token_url = settings.ACCESS_TOKEN_URL
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=token_url, client_id=client_id,
        client_secret=client_secret, verify=verify)
    return token