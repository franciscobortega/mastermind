from flask import Flask, jsonify, redirect, render_template, request, session, url_for
import requests
from flask_socketio import SocketIO, emit, join_room
from random import randint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('connect')
def handle_connect():
    unique_id = request.sid
    join_room('lobby')
    emit('user_connected', {'user_id': unique_id}, room='lobby')

@socketio.on('disconnect')
def handle_disconnect():
    print('WebSocket disconnected')

# TESTING WEBSOCKET
@socketio.on('lobby_message')
def handle_lobby_message(message):
    unique_id = request.sid 
    emit('lobby_message', {'message': message, 'user_id': unique_id}, room='lobby', include_self=True)

# constant and global variables
num_attempts = 10
game_over = False;
guessed = False;
rooms = {}

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

@app.route('/', methods=['POST', 'GET'])
def home_screen():
    """Render the home screen."""
    session.clear()
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        join = request.form.get('join', False)
        create = request.form.get('create', False)

        if not name:
            return render_template('index.html', error="Please enter a name.", code=code, name=name)
        
        if join != False and not code:
            return render_template('index.html', error="Please enter a game code.", code=code, name=name)
        
        room = code

        if create != False:
            # TODO: generate unique game room code
            room = 'ABCD'
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template('index.html', error="Room does not exist.", code=code, name=name)

        session["room"] = room
        session["name"] = name

        return redirect(url_for('load_lobby'))
        
    return render_template('index.html')

@app.route('/start_single')
def start_single_game():
    """Start a single-player game."""
    # Generate a random 4-digit code
    code = generate_code()

    return render_template('game.html', code=code, num_attempts=num_attempts)

@app.route('/start_multi')
def start_multiplayer_game():
    """Start a multiplayer game."""
    # TODO: have host generate a random 4-digit code
    code = 1234

    return render_template('multiplayer-game.html', code=code, num_attempts=num_attempts)

@app.route('/lobby')
def load_lobby():
    """Display lobby for multiplayer game."""
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for('home_screen'))
    

    return render_template('lobby.html')

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
    socketio.run(app, debug=True)