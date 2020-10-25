import requests

def check_response(response):
    if response.status_code == 200:
        return
    if response.status_code == 404:
        if response.json()["error"] == "Character is not in a fleet":
            raise CharacterNotInFleetError(response)
        if response.json()["error"] == "The fleet does not exist or you don't have access to it!":
            raise CharacterNotFCError(response)
            
    raise ESIError(response)

class ESIError(Exception):
    def __init__(self, response):
        message = f"Code {response.status_code}:  {response.text}"
        super().__init__(message)
        
class CharacterNotInFleetError(ESIError):
    pass

class CharacterNotFCError(ESIError):
    pass

class NotAuthedError(Exception):
    pass
    