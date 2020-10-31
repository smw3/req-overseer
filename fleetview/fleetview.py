import logging
import configparser
from flask import Flask, redirect, request, url_for, render_template, session
app = Flask(__name__)
app.config['SECRET_KEY'] = 'I am a long string with no measfkasf'    
app.config['BETA'] = True

config = configparser.ConfigParser()
if app.config['BETA']:
    config.read('/var/conf/fleetview/beta.conf')
else:
    config.read('/var/conf/fleetview/live.conf')

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

from .util.esi.esi_manager import requires_auth, get_auth_url, fetch_access_token, is_authenticated, get_authed_info
from .api.fleet_info import current_fleet

def is_beta():
    return app.config['BETA']

app.jinja_env.globals.update(is_beta=is_beta)

@app.route('/')
def index():    
    return redirect(url_for('show_fleet'))

@app.route('/show_fleet')
def show_fleet():    
    return render_template('show_fleet.html',
                           auth_url = url_for('auth', next=url_for('show_fleet')),
                           authed = is_authenticated(),
                           authed_info = get_authed_info())

@app.route('/show_snapshot/<char_id>/<snapshot_id>')
def show_snapshot(char_id, snapshot_id):    
    return render_template('show_snapshot.html', 
                           auth_url = url_for('auth', next=url_for('show_snapshot', char_id=char_id, snapshot_id=snapshot_id)),
                           authed = is_authenticated(),
                           authed_info = get_authed_info(),
                           char_id = char_id,
                           snapshot_id = snapshot_id)

@app.route('/show_shared/<share_id>')
def show_shared(share_id):    
    return render_template('show_shared.html', 
                           share_id = share_id,
                           auth_url = url_for('auth', next=url_for('show_shared', share_id = share_id)),
                           authed = is_authenticated(),
                           authed_info = get_authed_info())

@app.route('/unauth')
def unauth(): 
    if 'access_token' in session:
        del session['access_token']
    if 'access_token_time' in session:
        del session['access_token_time']
    
    return render_template('generic.html', 
                           message = "Unauthed!",
                           auth_url = url_for('auth', next=url_for('show_fleet')),
                           authed = is_authenticated(),
                           authed_info = get_authed_info())

@app.route('/auth', methods=['GET'])
def auth():
    return redirect(get_auth_url(request.args.get('next','')))

@app.route('/oauth-callback', methods=['GET'])
def oauth_callback():
    fetch_access_token(client_code = request.args.get('code',None))    
    redirect_target = request.args.get('state', url_for('index'))
    
    return redirect(redirect_target)
