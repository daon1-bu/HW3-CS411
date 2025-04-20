from app import create_app, db
from app.models import User, Boxer
import hashlib
import os

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    salt = os.urandom(16).hex()
    raw_password = "password123"
    hashed_password = hashlib.sha256((salt + raw_password).encode()).hexdigest()

    user = User(username="testuser", salt=salt, password=hashed_password)
    db.session.add(user)

    boxers = [
        Boxer(name="Mike Tyson", weight=220, height=5.8, reach=71, age=30, fights=58, wins=50, weight_class="Heavyweight"),
        Boxer(name="Manny Pacquiao", weight=147, height=5.5, reach=67, age=42, fights=72, wins=62, weight_class="Welterweight"),
        Boxer(name="Canelo Alvarez", weight=168, height=5.8, reach=70, age=33, fights=64, wins=60, weight_class="Super Middleweight"),
    ]

    db.session.add_all(boxers)
    db.session.commit()
    print("✅ Database seeded.")
