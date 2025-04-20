from flask import Flask, request, redirect
from .extensions import db, login_manager
from .models import User, Boxer
from .cache import BoxerCache
from flask_login import login_user, login_required, current_user
import hashlib

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)

    boxer_cache = BoxerCache()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route("/fight/<int:boxer_id>")
    def fight(boxer_id):
        boxer = boxer_cache.get_boxer(boxer_id)
        return f"{boxer.name} is ready to fight!" if boxer else "Boxer not found"

    @app.route("/profile")
    @login_required
    def profile():
        return f"Hello, {current_user.username}"

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            user = User.query.filter_by(username=username).first()
            if user:
                hashed = hashlib.sha256((user.salt + password).encode()).hexdigest()
                if hashed == user.password:
                    login_user(user)
                    return redirect("/profile")
            return "Invalid login"

        return """
        <form method=\"POST\">
            Username: <input name=\"username\"><br>
            Password: <input name=\"password\" type=\"password\"><br>
            <input type=\"submit\" value=\"Login\">
        </form>
        """

    with app.app_context():
        db.create_all()

    return app
