from flask import Flask, render_template
from random import randint

app = Flask(__name__)

def generate_code():
    """Generate a random 4-digit code."""
    code = []

    for _ in range(4):
        code.append(randint(0,7))

    return code 

@app.route('/')
def home_screen():
    """Render the home screen."""
    return render_template('index.html')

@app.route('/single')
def start_single_game():
    """Start a single-player game."""
    code = generate_code()
    return render_template('game.html', code=code)

if __name__ == '__main__':
    app.run(debug=True)