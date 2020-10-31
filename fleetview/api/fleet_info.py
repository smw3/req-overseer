from flask import Flask, redirect, request, url_for
import json
import configparser
import urllib.parse
import os
import time
import pytz

from pathlib import Path
from datetime import datetime

from ..fleetview import app, config
from ..util.esi.esi_manager import get_char_info, get_character_id
from ..util.esi.esi_calls import get_fleet_members, resolve_character_id, resolve_solar_system_id_to_name, mass_esi_request, resolve_ship_simple
from ..util.esi.esi_error import CharacterNotInFleetError, CharacterNotFCError, NotAuthedError, ESIError

@app.route('/api/fleet')
def current_fleet(): 
    share = request.args.get('sharing', default="false") == "true"
    try: 
        allowed_participants = urllib.parse.unquote(request.args.get('participants')).split(",")
    except:
        allowed_participants = []
    
    try:
        out = { "members" : [], "fleet_comp": {}, "ships": {}, "alliances": {}, "corporations": {} }
        app.logger.info("Query fleet under " + str(get_char_info()))
        
        fleet_info = get_fleet_members() 
        resolved_members = mass_resolve_fleet_members(fleet_info)
        app.logger.info("mass resolve member done")
        
        for member in fleet_info:
            member_dict = resolve_character_id(member["character_id"], resolved_members[member["character_id"]])
            member_dict = { **member, **member_dict }
            app.logger.info(f"Member dict: {member_dict}")
            
            member_dict["solar_system_name"] = resolve_solar_system_id_to_name(member_dict["solar_system_id"])
            
            ship_info = resolve_ship_simple(member_dict["ship_type_id"])
            member_dict["ship_info"] = ship_info
            
            # add ship type to fleet comp
            out["fleet_comp"][ship_info["type"]] = out["fleet_comp"].get(ship_info["type"],0) + 1
            out["ships"][ship_info["name"]] = out["ships"].get(ship_info["name"],0) + 1    
            
            # alliance/corp numbers
            out["alliances"][member_dict["alliance"]] = out["alliances"].get(member_dict["alliance"],0) + 1
            out["corporations"][member_dict["corp"]] = out["corporations"].get(member_dict["corp"],0) + 1   

            out["members"].append(member_dict)
            
            out["last_refresh"] = datetime.now(pytz.utc).strftime("%d %B %Y %H:%M:%S UTC")
            out["shared_to"] = allowed_participants
            
            if share:
                save_fleet_scan(out, get_character_id(), live = True)
                               
        return json.dumps(out)    
    except CharacterNotInFleetError:
        return '{"error": "You are not in a fleet!"}'
    except CharacterNotFCError:
        return '{"error": "The fleet does not exist or you don\'t have access to it! Are you the FC?"}'
    except NotAuthedError:
        return '{"error": "You need to authenticate first!" }'
    except ESIError:
        return '{"error": "Unknown ESI issue occured, please try again later." }'
    except Exception as inst:
        return f'{"error": "An unknown error occured: {inst}" }'
    
@app.route('/api/fleet/take_snapshot')
def take_fleet_snapshot(): 
    try:
        snapshot_id = int(round(time.time() * 1000))
        char_id = get_character_id()
        
        save_fleet_scan(current_fleet(), char_id, fleet_scan_name = f"{snapshot_id}")        
        
        out_dict = {}
        out_dict["char_id"] = char_id
        out_dict["snapshot_id"] = snapshot_id
        
        return json.dumps(out_dict)  
    except CharacterNotInFleetError:
        return '{"error": "You are not in a fleet!"}'
    except CharacterNotFCError:
        return '{"error": "The fleet does not exist or you don\'t have access to it! Are you the FC?"}'
    except NotAuthedError:
        return '{"error": "You need to authenticate first!" }'
    except ESIError:
        return '{"error": "Unknown ESI issue occured, please try again later." }'
    except Exception as inst:
        return f'{"error": "An unknown error occured: {inst}" }'   
    
def mass_resolve_fleet_members(fleet_info):
    member_ids = [member["character_id"] for member in fleet_info]
    
    resolved_members = mass_esi_request("characters/{par}/", [character_id for character_id in member_ids], public = True)
    
    return resolved_members
    
def save_fleet_scan(fleet_scan, char_id, live = False, fleet_scan_name = "none"):
    if live:
        base_path = config["DEFAULT"]["LIVE_SHARE"]
        livescan_path = f"{base_path}/{char_id}/live_scan.json"
        
        Path(f"{base_path}/{char_id}").mkdir(parents=True, exist_ok=True)
        
        json.dump( fleet_scan, open( livescan_path, 'w' ) )
    else:
        base_path = config["DEFAULT"]["SNAPSHOTS"]
        snapshot_path = f"{base_path}/{char_id}/{fleet_scan_name}.json"
        
        Path(f"{base_path}/{char_id}").mkdir(parents=True, exist_ok=True)
        
        json.dump( fleet_scan, open( snapshot_path, 'w' ) )        
    
@app.route('/api/shared_fleet/<sharer_char_id>')
def shared_fleet(sharer_char_id):
    base_path = config["DEFAULT"]["LIVE_SHARE"]
    livescan_path = f"{base_path}/{sharer_char_id}/live_scan.json"
    
    if os.path.exists(livescan_path):
        fleet_scan = json.load( open( livescan_path ) )
        
        try:
            if get_char_info()["CharacterName"] in fleet_scan["shared_to"]:
                return json.dumps(fleet_scan)
            else:
                return '{"error": "You were not authorized to see this fleet scan!" }'
        except NotAuthedError:
            return '{"error": "You need to authenticate first!" }'
    else:
        return '{"error": "No livescan by that character ID available!" }'
    
    
@app.route('/api/fleet/snapshot/<char_id>/<snapshot_id>')
def get_fleet_snapshot(char_id, snapshot_id):     
    base_path = config["DEFAULT"]["SNAPSHOTS"]
    snapshot_path = f"{base_path}/{char_id}/{snapshot_id}.json"
    
    if os.path.exists(snapshot_path):
        fleet_scan = json.load( open( snapshot_path ) )
        
        try:
            return fleet_scan
        except NotAuthedError:
            return '{"error": "You need to authenticate first!" }'
    else:
        return '{"error": "No livescan by that ID available!" }' 
