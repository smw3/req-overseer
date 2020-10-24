from flask import Flask, redirect, request, url_for

from ..fleetview import app
from ..util.esi.esi_manager import requires_auth
from ..util.esi.esi_calls import get_fleet_members, resolve_character_id
from ..util.esi.esi_error import CharacterNotInFleetError, CharacterNotFCError

@app.route('/api/fleet')
@requires_auth
def current_fleet():    
    try:
        out = { "members" : [] }
        for member in get_fleet_members():
            out["members"].append(resolve_character_id(member["character_id"]))
                               
        return str(out)    
    except CharacterNotInFleetError:
        return "Not in a fleet!"
    except CharacterNotFCError:
        return "You are not the FC!"