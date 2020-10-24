from functools import wraps
from flask import session, request, redirect, url_for
import requests
import time

from .esi_error import ESIError

CLIENT_ID = "34ff20b9719a4cad93cf30e433594150"
LOCAL_ADDRESS = "18.222.147.238"
LOCAL_PORT = "80"

SCOPES = ["esi-fleets.read_fleet.v1", "esi-fleets.write_fleet.v1"]

def is_authenticated():
    return "access_token" in session and session['access_token'] is not None
        
def requires_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            return redirect(url_for('auth', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def get_auth_url(state):
    response_type = "code"
    redirect_uri = f"http://{LOCAL_ADDRESS}:{LOCAL_PORT}/oauth-callback"

    client_id = CLIENT_ID
    scopes = "%20".join(SCOPES)
    
    return f"https://login.eveonline.com/oauth/authorize?response_type={response_type}&redirect_uri={redirect_uri}&client_id={client_id}&scope={scopes}&state={state}"
   
def fetch_access_token(client_code = None, refresh = False):
    SSO_ACCESS_TOKEN_URL = "https://login.eveonline.com/oauth/token"
    headers = {}
    headers['Content-Type'] = "application/x-www-form-urlencoded"
    headers['Authorization'] = "Basic MzRmZjIwYjk3MTlhNGNhZDkzY2YzMGU0MzM1OTQxNTA6c0ZiTWtla0JyZFhpWlhQOVJvT05EU1gzeTdNWnJ5M2tiazc0d0pOSA=="
    headers['User-Agent'] = "Requiem Eternal Fleetview"
    
    body = {}
    if refresh:
        body['grant_type'] = "refresh_token"
        body['refresh_token'] = session['access_token']['refresh_token']
    else:
        body['grant_type'] = "authorization_code"
        body['code'] = client_code
    
    req = requests.post(SSO_ACCESS_TOKEN_URL, headers = headers, data = body)
    
    if req.status_code == 200:
        session['access_token'] = req.json()
        session['access_token_time'] = time.time()

        assert(is_authenticated())
        return

    raise ESIError()
    
def get_access_token():
    if 'access_token_time' not in session:
        fetch_access_token(refresh = True)
        
    if time.time() > session['access_token_time'] + session['access_token']['expires_in']:
        fetch_access_token(refresh = True)
        
    return session['access_token']