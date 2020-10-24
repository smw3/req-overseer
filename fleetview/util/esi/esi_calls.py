import requests
from .esi_error import check_response
from .esi_manager import get_access_token

def get_char_info():
    url = "https://login.eveonline.com/oauth/verify"
    
    headers = {}
    headers['Authorization'] = "Bearer  " + get_access_token()['access_token']
    
    req = requests.get(url, headers = headers)
    check_response(req)

    return req.json()


def get_character_fleet():
    character_id = get_char_info()["CharacterID"]
    
    url = "https://esi.evetech.net/latest/characters/"+ str(character_id) + "/fleet/"
    
    headers = {}
    headers['Authorization'] = "Bearer  " + get_access_token()['access_token']
    
    body = {}
    body['datasource'] = "tranquility"
    
    req = requests.get(url, headers = headers, params = body)
    
    check_response(req)
    
    return req.json()

