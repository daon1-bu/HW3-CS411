from flask import request, redirect, Flask
from flask_login import login_user, logout_user, login_required, current_user
from . import db, login_manager
from .models import User, Boxer
from .cache import BoxerCache

app = Flask(__name__)
boxer_cache = BoxerCache()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    user = User.query.filter_by(username=username).first()
    if user:
        login_user(user)
        return redirect('/profile')
    return "Invalid login"

@app.route('/profile')
@login_required
def profile():
    return f"Hello {current_user.username}"

@app.route('/fight/<int:boxer_id>')
def fight(boxer_id):
    boxer = boxer_cache.get_boxer(boxer_id)
    return f"{boxer.name} is ready to fight!" if boxer else "Boxer not found"
