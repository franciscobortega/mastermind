from flask import Flask, render_template
import requests
from random import randint

app = Flask(__name__)

NUM_ATTEMPTS = 10

def generate_code():
    """Generate a random 4-digit code."""
    
    # base_url = "https://www.random.org/integers/"

    # payload = {'num': 4,
    #            'min': 0,
    #            'max': 7,
    #            'col': 1,
    #            'base': 10,
    #            'format': 'plain',
    #            'rnd': 'new'}

    # response = requests.get(base_url, params=payload)

    # print(response.text) # prints plain text response, with one integer per line.

    code = []

    for _ in range(4):
        code.append(randint(0,7))


    return code 

def check_guess(secret_code, guess):
    correct_numbers = 0
    correct_locations = 0

    for index, num in enumerate(guess):
        if num in secret_code:
            correct_numbers += 1

        if num == secret_code[index]:
            correct_locations += 1

    # Did the player guess any number correctly?
    if correct_numbers == 0 and correct_locations == 0:
        return "all incorrect"
    # Are any numbers in the correct location?
    else:
        return f"{correct_numbers} correct numbers and {correct_locations} correct locations"

@app.route('/')
def home_screen():
    """Render the home screen."""
    return render_template('index.html')

@app.route('/start_single')
def start_single_game():
    """Start a single-player game."""
    code = generate_code()
    return render_template('game.html', code=code, NUM_ATTEMPTS=NUM_ATTEMPTS)

@app.route('/guess', methods=['POST'])
def evaluate_guess():
    """Evaluate the player's guess."""
    pass

@app.route('/end', methods=['POST'])
def end_game():
    """End the game."""
    pass

if __name__ == '__main__':
    app.run(debug=True)