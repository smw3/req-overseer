from flask import Flask, redirect, request, url_for

from ..fleetview import app
from ..util.esi.esi_manager import requires_auth, get_auth_url, fetch_access_token
from ..util.esi.esi_calls import get_char_info, get_fleet_members
from ..util.esi.esi_error import CharacterNotInFleetError

@app.route('/api/fleet')
@requires_auth
def current_fleet():    
    try:
        return get_fleet_members()
    except CharacterNotInFleetError:
        return {}