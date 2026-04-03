from register.register import register_blueprint
from login.login import login_blueprint
from flask import *
import data.data_check  
from functools import wraps
# initialize the database
data.data_check.init_db()


app = Flask(__name__)
app.secret_key = 'supersecretkey' # Needed for flashing messages

# Register Blueprints
app.register_blueprint(register_blueprint, url_prefix='/auth')
app.register_blueprint(login_blueprint, url_prefix='/auth')

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login.login'))
        return f(*args, **kwargs)
    return decorated


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)
