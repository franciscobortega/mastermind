"""CRUD operations for Mastermind."""

from model import db, User, connect_to_db

def create_user(username, password, total_wins):
    """Create and return a new user."""

    user = User(username=username, password=password, total_wins=total_wins)

    return user

def update_user_score(data):
    """Update an existing user's score."""
    user = get_user_by_username(data.username)

    user.total_wins = data.total_wins

    db.session.commit()

    return user

def get_users():
    """Return all users."""

    return User.query.all()

def get_user_by_id(user_id):
    """Return user by id."""

    return User.query.get(user_id)

def get_user_by_username(username):
    """Return user by username."""

    return User.query.filter(User.username == username).first()

def get_top_players():
    """Return top players."""

    return User.query.order_by(User.total_wins.desc()).limit(3).all()

if __name__ == '__main__':
    from app import app
    connect_to_db(app)