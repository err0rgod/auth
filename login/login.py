import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
import bcrypt
from sqlite3 import connect

# create a login blueprint
login_blueprint = Blueprint('login', __name__, template_folder='templates')

@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        try:
            conn = connect('data/data.db')
            cursor = conn.cursor()
            
            # 1. Fetch user's password from DB
            cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            
            if result:
                stored_password = result[0]
                # 2. Check if the entered password matches the stored hash
                if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                    
                    # 3. GENERATE TOKEN: Identity is usually the username or unique user ID
                    access_token = create_access_token(identity=username)
                    flash(f'Welcome back, {username}!', 'success')
                    
                    # 4. SET TOKEN IN COOKIES: 
                    # We create a response object first to attach the token cookie
                    response = make_response(redirect(url_for('profile')))
                    set_access_cookies(response, access_token)
                    return response
                else:
                    flash('Invalid username or password.', 'error')
            else:
                flash('Invalid username or password.', 'error')
                
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
        finally:
            if 'conn' in locals():
                conn.close()
            
    return render_template('login.html')

@login_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    # 5. LOGOUT: 
    # To logout, we clear the JWT token cookie from the browser
    flash('You have been logged out.', 'success')
    response = make_response(redirect(url_for('login.login')))
    unset_jwt_cookies(response)
    return response
