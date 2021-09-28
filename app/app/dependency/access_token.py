from starlette_context import context
import requests

from urllib.request import urlopen
import json
from jose import jwt

tokens = {}

# Retrieve access token for machine to machine calls and stores into memory for subsequent calls.
# During subsequent calls, validates token from memory
# If token validation fails, fresh token is retrieved.

def get_access_token():

    token_key = "API_ACCESS_TOKEN"

    auth0_domain = context["AUTH0_DOMAIN"]
    api_identifier = context["AUTH0_API_IDENTIFIER"]
    client_id = context["AUTH0_API_CLIENT_ID"]
    client_secret = context["AUTH0_API_CLIENT_SECRET"]

    if token_key not in tokens or not validate_access_token(tokens[token_key], api_identifier, auth0_domain):
        access_token = retrieve_access_token(client_id, client_secret, api_identifier, auth0_domain)
        tokens[token_key] = access_token
    else:
        access_token = tokens[token_key]

    return access_token


def validate_access_token(access_token, api_identifier, auth0_domain):
    ALGORITHMS = context["AUTH0_ALGORITHMS"]
    
    jsonurl = urlopen("https://"+auth0_domain+"/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    try:
        unverified_header = jwt.get_unverified_header(access_token)
    except jwt.JWTError:
        return False
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            jwt.decode(
                access_token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=api_identifier,
                issuer="https://"+auth0_domain+"/"
            )
        except jwt.ExpiredSignatureError:
            return False
        except jwt.JWTClaimsError:
            return False
        except Exception:
            return False
        return True
    return False

def retrieve_access_token(client_id, client_secret, api_identifier, auth0_domain):
    url = "https://"+ auth0_domain + "/oauth/token"
    payload = {'grant_type': 'client_credentials', 'client_id': client_id, 'client_secret': client_secret, 'audience': api_identifier}
    headers = { 'content-type': "application/x-www-form-urlencoded" }

    resp = requests.post(url, data=payload, headers=headers)
    respData = resp.json()
    access_token = respData["access_token"]

    return access_token