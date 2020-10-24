import requests
from .esi_error import check_response
from .esi_manager import get_access_token, get_character_id
from .esi_error import ESIError

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def esi_request(endpoint, public = False):    
    url = "https://esi.evetech.net/latest/" + endpoint
    
    headers = {}
    if not public:
        headers['Authorization'] = "Bearer  " + get_access_token()['access_token']
    headers['User-Agent'] = "Requiem Eternal Notification Relay"
    
    body = {}
    body['datasource'] = "tranquility"
    
    logger.info("ESI: " + url)
    
    req = requests.get(url, headers = headers, params = body)
    
    if req.status_code == 200:
        return req.json() 
    elif req.status_code == 403:
        if get_access_token():
            esi_request(endpoint, public = public)
    else:
        logger.error("ESI Request got unexpected response: ")
        logger.error(req.status_code)
        logger.error(req.text)
        check_response(req) 

def get_character_fleet():
    character_id = get_character_id()
    return esi_request(f"characters/{character_id}/fleet/")

def get_fleet_members():
    fleet_id = get_character_fleet()["fleet_id"]
    return esi_request(f"fleets/{fleet_id}/members")