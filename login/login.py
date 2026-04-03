import json
from flask import *
import bcrypt
from sqlite3 import *
# create a login blueprint
login_blueprint = Blueprint('login', __name__, template_folder='templates')

# create a login route
@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        try:
            conn = connect('data/data.db')
            cursor = conn.cursor()
            # 1. Fetch the user's password in one go
            cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            
            if result:
                # 2. Compare the entered password with the hashed password from DB
                stored_password = result[0]
                if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                    # 3. Success: Set the session and redirect
                    session['user'] = username
                    flash(f'Welcome back, {username}!', 'success')
                    return redirect(url_for('profile'))
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
    session.pop('user', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login.login'))
