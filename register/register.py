from flask import *
from json import *
import bcrypt
from sqlite3 import *
register_blueprint = Blueprint('register',__name__,template_folder='templates')


# create a register route
@register_blueprint.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # check if user already exists
        try:
            conn = connect('data/data.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            if cursor.fetchone():
                flash('User already exists!')
                return redirect(url_for('register.register'))
        except FileNotFoundError:
            pass
        except Exception as e:
            flash(f'An error occurred: {str(e)}')
            return redirect(url_for('register.register'))
        # converting password to hash
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')
        # inserting the data in database
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()    
        
        # redirecting to login page
        flash(f'Registration succesfull for {username}!')
        return redirect(url_for('login.login'))
    return render_template('register.html')
