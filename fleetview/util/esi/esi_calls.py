from ...fleetview import app

import requests
from .esi_error import check_response
from .esi_manager import get_access_token, get_character_id
from .esi_error import ESIError

import cachetools.func

def esi_request(endpoint, public = False):    
    url = "https://esi.evetech.net/latest/" + endpoint
    
    headers = {}
    if not public:
        headers['Authorization'] = "Bearer  " + get_access_token()['access_token']
    headers['User-Agent'] = "Requiem Eternal Notification Relay"
    
    body = {}
    body['datasource'] = "tranquility"
    
    app.logger.info("ESI: " + url)
    
    req = requests.get(url, headers = headers, params = body)
    
    if req.status_code == 200:
        app.logger.info("  : " + str(req.json()))
        return req.json() 
    elif req.status_code == 403:
        if get_access_token():
            return esi_request(endpoint, public = public)
    else:
        app.logger.error("ESI Request got unexpected response: ")
        app.logger.error(req.status_code)
        app.logger.error(req.text)
        check_response(req) 

def get_character_fleet():
    character_id = get_character_id()
    return esi_request(f"characters/{character_id}/fleet/")

def get_fleet_members():
    fleet_id = get_character_fleet()["fleet_id"]
    return esi_request(f"fleets/{fleet_id}/members")

def resolve_ship_simple(type_id):
    type_dict = resolve_type_id(type_id)
    
    new_dict = {}
    new_dict["name"] = type_dict["name"]
    new_dict["type"] = resolve_group_id(type_dict["group_id"])["name"]
        
    return new_dict

def resolve_type_id_to_name(type_id):
    return resolve_type_id(type_id)["name"]

@cachetools.func.ttl_cache(maxsize=128, ttl=480 * 60 * 60)
def resolve_type_id(type_id):
    return esi_request(f"universe/types/{type_id}/", public = True)

@cachetools.func.ttl_cache(maxsize=128, ttl=480 * 60 * 60)
def resolve_dogma_attribute(attribute_id):
    return esi_request(f"dogma/attributes/{attribute_id}/", public = True)

@cachetools.func.ttl_cache(maxsize=128, ttl=480 * 60 * 60)
def resolve_group_id(group_id):
    return esi_request(f"universe/groups/{group_id}/", public = True)

@cachetools.func.ttl_cache(maxsize=128, ttl=480 * 60 * 60)
def resolve_solar_system_id_to_name(system_id):
    return esi_request(f"universe/systems/{system_id}/", public = True)["name"]

@cachetools.func.ttl_cache(maxsize=128, ttl=480 * 60 * 60)
def resolve_corporation_id_to_name(corporation_id):
    return esi_request(f"corporations/{corporation_id}/", public = True)["name"]

@cachetools.func.ttl_cache(maxsize=128, ttl=480 * 60 * 60)
def resolve_alliance_id_to_name(alliance_id):
    return esi_request(f"alliances/{alliance_id}/", public = True)["name"]

@cachetools.func.ttl_cache(maxsize=128, ttl=48 * 60 * 60)
def resolve_character_id(character_id):
    out_dict = {}
    esi_dict = esi_request(f"characters/{character_id}/", public = True)
    out_dict["name"] = esi_dict["name"]
    out_dict["corp"] = resolve_corporation_id_to_name(esi_dict["corporation_id"])
    out_dict["alliance"] = resolve_alliance_id_to_name(esi_dict["alliance_id"])
    return out_dict