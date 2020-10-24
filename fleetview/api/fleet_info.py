from flask import Flask, redirect, request, url_for

from ..fleetview import app
from ..util.esi.esi_manager import requires_auth, get_auth_url, fetch_access_token
from ..util.esi.esi_calls import get_fleet_members
from ..util.esi.esi_error import CharacterNotInFleetError

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/api/fleet')
@requires_auth
def current_fleet():    
    try:
        return str(get_fleet_members())
    except CharacterNotInFleetError:
        return {}