from flask import Flask, redirect, request, url_for

from ..fleetview import app
from ..util.esi.esi_manager import requires_auth
from ..util.esi.esi_calls import get_fleet_members, resolve_character_id, resolve_solar_system_id_to_name, resolve_ship_simple
from ..util.esi.esi_error import CharacterNotInFleetError, CharacterNotFCError

@app.route('/api/fleet')
@requires_auth
def current_fleet():    
    try:
        out = { "members" : [], "fleet_comp": {}, "ships": {} }
        for member in get_fleet_members():
            member_dict = resolve_character_id(member["character_id"])
            member_dict = {**member, **member_dict}
            
            member_dict["solar_system_name"] = resolve_solar_system_id_to_name(member_dict["solar_system_id"])
            
            ship_info = resolve_ship_simple(member_dict["ship_type_id"])
            member_dict["ship_info"] = ship_info
            
            # add ship type to fleet comp
            out["fleet_comp"][ship_info["type"]] = out["fleet_comp"].get(ship_info["type"],0) + 1
            out["ships"][ship_info["type"]] = out["ships"].get(ship_info["name"],0) + 1    

            out["members"].append(member_dict)
            
        
                               
        return str(out)    
    except CharacterNotInFleetError:
        return "Not in a fleet!"
    except CharacterNotFCError:
        return "You are not the FC!"