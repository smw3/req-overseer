from flask import Flask, redirect, request, url_for
import json
import configparser
import urllib.parse
import os
from datetime import datetime

from ..fleetview import app, config
from ..util.esi.esi_manager import get_char_info, get_character_id
from ..util.esi.esi_calls import get_fleet_members, resolve_character_id, resolve_solar_system_id_to_name, resolve_ship_simple
from ..util.esi.esi_error import CharacterNotInFleetError, CharacterNotFCError, NotAuthedError

@app.route('/api/fleet')
def current_fleet(): 
    share = request.args.get('sharing', default="false") == "true"
    allowed_participants = ",".split(urllib.parse.unquote(request.args.get('participants')))
    
    try:
        out = { "members" : [], "fleet_comp": {}, "ships": {} }
        app.logger.info("Query fleet under " + str(get_char_info()))
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
            
            out["last_refresh"] = datetime.now().strftime("%H:%M:%S")
            out["shared_to"] = allowed_participants
            
            if share:
                save_fleet_scan(out, get_character_id())
                               
        return json.dumps(out)    
    except CharacterNotInFleetError:
        return '{"error": "You are not in a fleet!"}'
    except CharacterNotFCError:
        return '{"error": "The fleet does not exist or you don\'t have access to it! Are you the FC?"}'
    except NotAuthedError:
        return '{"error": "You need to authenticate first!" }'
    
def save_fleet_scan(fleet_scan, char_id):
    base_path = config["DEFAULT"]["LIVE_SHARE"]
    livescan_path = base_path + "/" + char_id + "/" + "live_scan.json"
    
    os.mkdir(base_path + "/" + char_id)
    
    os.remove(livescan_path)
    json.dump( fleet_scan, open( livescan_path, 'w' ) )
    
@app.route('/api/shared_fleet/<sharer_char_id>')
def shared_fleet(sharer_char_id):
    base_path = config["DEFAULT"]["LIVE_SHARE"]
    livescan_path = base_path + "/" + sharer_char_id + "/" + "live_scan.json"
    
    if os.path.exists(livescan_path):
        fleet_scan = json.load( open( livescan_path ) )
        
        try:
            if get_char_info()["CharacterName"] in fleet_scan["shared_to"]:
                return json.dumps(fleet_scan)
            else:
                return '{"error": "You were not authorized to see this fleet scan!" }'
        except NotAuthedError:
            return '{"error": "You need to authenticate first!" }'
        
        return fleet_scan
    else:
        return '{"error": "No livescan by that character ID available!" }'
    
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