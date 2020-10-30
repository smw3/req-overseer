import requests

def parallel_esi_request(endpoint, access_token = None):    
    url = "https://esi.evetech.net/latest/" + endpoint
    
    headers = {}
    if access_token is not None:
        headers['Authorization'] = "Bearer  " + access_token
    headers['User-Agent'] = "Requiem Eternal Notification Relay"
    
    body = {}
    body['datasource'] = "tranquility"
    
    req = requests.get(url, headers = headers, params = body)
    
    if req.status_code == 200:
        return req.json() 
    
    return None
        
def single_mass_request(endpoint, parameter, access_token = False):
    out = parallel_esi_request(endpoint, access_token)
    out["esi_request_var"] = parameter
    
    return out