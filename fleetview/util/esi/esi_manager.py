from ...fleetview import app, config

from functools import wraps
from flask import session, request, redirect, url_for
import requests
import time
import base64

import cachetools.func
import configparser

from .esi_error import ESIError, check_response, NotAuthedError



CLIENT_ID = config['DEFAULT']['CLIENT_ID']
auth_string = CLIENT_ID + ":" + config['DEFAULT']['SECRET_KEY']
AUTHORIZATION = base64.b64encode(auth_string.encode('ascii')).decode('ascii')
LOCAL_ADDRESS = config['DEFAULT']['LOCAL_ADDRESS']
LOCAL_PORT = config['DEFAULT']['LOCAL_PORT']

SCOPES = ["esi-fleets.read_fleet.v1"]

def is_authenticated():
    return "access_token" in session and session['access_token'] is not None

def get_character_id():
    if "character_id" in session and is_authenticated():
        return session['character_id']
    
    session['character_id'] = get_char_info()['CharacterID']
    return session['character_id']
    
def get_char_info():
    url = "https://login.eveonline.com/oauth/verify"
    
    headers = {}
    headers['Authorization'] = "Bearer  " + get_access_token()['access_token']
    
    req = requests.get(url, headers = headers)
    check_response(req)

    return req.json()

def get_authed_info():
    if not is_authenticated():
        return {}
    
    return get_char_info()
        
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
    headers['Authorization'] = "Basic " + AUTHORIZATION
    headers['User-Agent'] = "Requiem Eternal Fleetview"
    
    body = {}
    if refresh:
        if 'access_token' not in session:
            raise NotAuthedError()
            
        body['grant_type'] = "refresh_token"
        body['refresh_token'] = session['access_token']['refresh_token']
    else:
        if client_code is None:
            raise NotAuthedError()
            
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