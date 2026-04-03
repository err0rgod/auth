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
        
        found = False
        # checking if the user is registered
        try:
            conn = connect('data/data.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            if cursor.fetchone():
                found = True
                cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
                if bcrypt.checkpw(password.encode('utf-8'), cursor.fetchone()[0].encode('utf-8')):
                    found = True
                    session['user'] = username
                    flash(f'Welcome back, {username}!', 'success')
                    return redirect(url_for('profile'))
                else:
                    found = False
                    flash('Invalid username or password.', 'error')
                    return render_template('login.html')
            else:
                flash('Invalid username or password.', 'error')
                return render_template('login.html')
        except FileNotFoundError:
            flash('No users registered yet!', 'error')
            return render_template('register.html')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            return render_template('register.html')
        finally:
            conn.close()
            
        if found:
            session['user'] = username
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Invalid username or password.', 'error')
            
    return render_template('login.html')



@login_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login.login'))
