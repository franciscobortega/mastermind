"""Script to seed database."""

import os
from app import app
import crud
import model

def seed_database():
    os.system("dropdb mastermind")
    os.system('createdb mastermind')

    model.connect_to_db(app)
    model.db.create_all()

    # --------------- Seed user --------------- #
    username = 'bryanortega'
    password = '1234'
    total_wins = 100

    # create and add new user to db
    new_user = crud.create_user(username, password, total_wins)
    model.db.session.add(new_user)

    model.db.session.commit()

# Work within application context
if __name__ == "__main__":
    with app.app_context():
        seed_database()
