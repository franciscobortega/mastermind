from flask import Flask, jsonify, render_template, request
import requests
from random import randint

app = Flask(__name__)

# constant and global variables
num_attempts = 10
game_over = False;
guessed = False;

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
    """Evaluate the player's guess."""
    global game_over, num_attempts, guessed

    # Convert user's guess and secret code into lists
    guess = [int(x) for x in guess]
    #TODO: secret code is being converted into a string at some point between the client-server or server-client transmissions.
    # potentially store server-side via as a session variable or as part of the database
    secret_code = secret_code.strip('][').split(', ')
    secret_code = [int(x) for x in secret_code]

    # Validate the user's guess input
    # TODO: make sure that the user's guess falls within the expected range
    if len(guess) != 4:
        return "Please enter a 4-digit guess."

    #TODO: Add additional mechanism to handle game over state
    if game_over and guessed:
        return "Game Over. The correct code was already guessed."
    
    # End game if user had exhausted all attempts
    if num_attempts <= 0:
        game_over = True
        return f"Game Over. No more attempts. The secret code was {secret_code}."
    
    num_attempts -= 1

    # End game if the guess is a full match with the secret code
    if guess == secret_code:
        game_over = True
        guessed = True
        return "You won! You guessed the code correctly!"
    
    correct_numbers = 0
    correct_locations = 0

    # print(guess, secret_code)

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
    # Generate a random 4-digit code
    code = generate_code()

    return render_template('game.html', code=code, num_attempts=num_attempts)

@app.route('/start_multi')
def start_multiplayer_game():
    """Start a multi-player game."""
    print("Starting multi-player game...")

@app.route('/guess', methods=['POST'])
def evaluate_guess():
    """Evaluate the player's guess."""
    # Extract the user's guess and secret code from the form data
    user_guess = request.form.get('guess')
    secret_code = request.form.get('secret_code')

    # print(user_guess, secret_code)

    # Process the user's guess against the secret code
    feedback = check_guess(secret_code, user_guess) 

    # Return feedback as JSON
    return jsonify({'feedback': feedback})

@app.route('/end', methods=['POST'])
def end_game():
    """End the game."""
    pass

if __name__ == '__main__':
    app.run(debug=True)