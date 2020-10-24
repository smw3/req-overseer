from flask import Flask, redirect, request, url_for, render_template
app = Flask(__name__)
app.config['SECRET_KEY'] = 'I am a long string with no measfkasf'    

from .util.esi.esi_manager import requires_auth, get_auth_url, fetch_access_token
from .api.fleet_info import current_fleet

@app.route('/')
@requires_auth
def index():    
    return "Hello world"

@app.route('/show_fleet')
@requires_auth
def show_fleet():    
    return render_template('template/show_fleet.html')

@app.route('/auth', methods=['GET'])
def auth():
    return redirect(get_auth_url(request.args.get('next','')))

@app.route('/oauth-callback', methods=['GET'])
def oauth_callback():
    fetch_access_token(client_code = request.args.get('code',None))    
    redirect_target = request.args.get('state', url_for('index'))
    
    return redirect(redirect_target)
