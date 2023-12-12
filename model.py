"""Models for Mastermind."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True, )
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    total_wins = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<User user_id={self.user_id} username={self.username}>'
    

def connect_to_db(flask_app, db_uri="postgresql:///mastermind", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the database!")


if __name__ == "__main__":
    from app import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)