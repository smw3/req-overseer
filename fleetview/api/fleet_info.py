from flask import Flask, redirect, request, url_for
import json

from ..fleetview import app
from ..util.esi.esi_manager import requires_auth
from ..util.esi.esi_calls import get_fleet_members, resolve_character_id, resolve_solar_system_id_to_name, resolve_ship_simple
from ..util.esi.esi_error import CharacterNotInFleetError, CharacterNotFCError, NotAuthedError

@app.route('/api/fleet')
def current_fleet():    
    try:
        out = { "members" : [], "fleet_comp": {}, "ships": {} }
        for member in get_fleet_members():
            member_dict = resolve_character_id(member["character_id"])
            member_dict = { **member, **member_dict }
            
            member_dict["solar_system_name"] = resolve_solar_system_id_to_name(member_dict["solar_system_id"])
            
            ship_info = resolve_ship_simple(member_dict["ship_type_id"])
            member_dict["ship_info"] = ship_info
            
            # add ship type to fleet comp
            out["fleet_comp"][ship_info["type"]] = out["fleet_comp"].get(ship_info["type"],0) + 1
            out["ships"][ship_info["name"]] = out["ships"].get(ship_info["name"],0) + 1    

            out["members"].append(member_dict)
                               
        return json.dumps(out)    
    except CharacterNotInFleetError:
        return '{"error": "You are not in a fleet!"}'
    except CharacterNotFCError:
        return '{"error": "The fleet does not exist or you don\'t have access to it! Are you the FC?"}'
    except NotAuthedError:
        return '{"error": "You need to authenticate first!" }'
    
    
    
@app.route('/api/mock/fleet')
def current_fleet_mock():
    return '''{
	"members": [
		{
			"character_id": 1581768186,
			"join_time": "2020-10-24T17:32:56Z",
			"role": "fleet_commander",
			"role_name": "Fleet Commander (Boss)",
			"ship_type_id": 670,
			"solar_system_id": 30002619,
			"squad_id": -1,
			"takes_fleet_warp": true,
			"wing_id": -1,
			"name": "IHaveAShortName",
			"corp": "Pipebomb Pinata",
			"alliance": "Requiem Eternal",
			"solar_system_name": "6E-MOW",
			"ship_info": {
				"name": "Capsule",
				"type": "Capsule"
			}
		},
		{
			"character_id": 1581768186,
			"join_time": "2020-10-24T17:32:56Z",
			"role": "fleet_commander",
			"role_name": "Fleet Commander (Boss)",
			"ship_type_id": 670,
			"solar_system_id": 30002619,
			"squad_id": -1,
			"takes_fleet_warp": true,
			"wing_id": -1,
			"name": "IHaveAShortName",
			"corp": "Pipebomb Pinata",
			"alliance": "Requiem Eternal",
			"solar_system_name": "6E-MOW",
			"ship_info": {
				"name": "Capsule",
				"type": "Capsule"
			}
		},
		{
			"character_id": 1581768186,
			"join_time": "2020-10-24T17:32:56Z",
			"role": "fleet_commander",
			"role_name": "Fleet Commander (Boss)",
			"ship_type_id": 670,
			"solar_system_id": 30002619,
			"squad_id": -1,
			"takes_fleet_warp": true,
			"wing_id": -1,
			"name": "IHaveAShortName",
			"corp": "Pipebomb Pinata",
			"alliance": "Requiem Eternal",
			"solar_system_name": "6E-MOW",
			"ship_info": {
				"name": "Capsule",
				"type": "Capsule"
			}
		}
	],
	"fleet_comp": {
		"Capsule": 3
	},
	"ships": {
		"Capsule": 3
	}
}'''