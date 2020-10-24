import logging
from flask import Flask, redirect, request, url_for, render_template
app = Flask(__name__)
app.config['SECRET_KEY'] = 'I am a long string with no measfkasf'    

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

from .util.esi.esi_manager import requires_auth, get_auth_url, fetch_access_token
from .api.fleet_info import current_fleet, current_fleet_mock

@app.route('/')
def index():    
    return "Hello world"

@app.route('/show_fleet')
def show_fleet():    
    return render_template('show_fleet.html')

@app.route('/auth', methods=['GET'])
def auth():
    return redirect(get_auth_url(request.args.get('next','')))

@app.route('/oauth-callback', methods=['GET'])
def oauth_callback():
    fetch_access_token(client_code = request.args.get('code',None))    
    redirect_target = request.args.get('state', url_for('index'))
    
    return redirect(redirect_target)
