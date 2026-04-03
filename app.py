from register.register import register_blueprint
from login.login import login_blueprint
from flask import Flask, render_template, redirect, url_for
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, verify_jwt_in_request
import data.data_check  

# initialize the database
data.data_check.init_db()

app = Flask(__name__)

# Secret keys are used to sign the tokens/sessions so they can't be tampered with
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['JWT_SECRET_KEY'] = 'jwt-super-secret-key' 

# IMPORTANT: We tell JWT to look for tokens in Cookies (more secure for web apps)
app.config['JWT_TOKEN_LOCATION'] = ['cookies']

# CSRF protection is disabled for this prototype but recommended for production
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

# Initialize the JWT Manager
jwt = JWTManager(app)

# --- JWT ERROR HANDLERS ---
# If a user tries to access a protected page without a token, redirect to login
@jwt.unauthorized_loader
def unauthorized_callback(callback):
    return redirect(url_for('login.login'))

# If the token is expired or tampered with, redirect to login
@jwt.invalid_token_loader
def invalid_token_callback(callback):
    return redirect(url_for('login.login'))

# Register Blueprints
app.register_blueprint(register_blueprint, url_prefix='/auth')
app.register_blueprint(login_blueprint, url_prefix='/auth')

# --- CONTEXT PROCESSOR ---
# This makes the 'current_user' variable available in every HTML template automatically
@app.context_processor
def inject_user():
    try:
        # Check for JWT but don't force it (optional=True)
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity() # Gets the username from the token
        return {'current_user': identity}
    except Exception:
        # No token found, so no user is logged in
        return {'current_user': None}

@app.route('/')
@jwt_required() # Protects this route: redirect if not logged in
def index():
    return render_template('index.html')

@app.route('/profile')
@jwt_required() # Only accessible with a valid JWT token
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)
