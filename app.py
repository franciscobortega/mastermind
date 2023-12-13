from flask import Flask, jsonify, redirect, render_template, request, session, url_for
import requests
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from random import randint, choice
from string import ascii_uppercase
from model import connect_to_db, db
import crud

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# constant and global variables
num_attempts = 10
game_over = False;
guessed = False;
rooms = {}

@socketio.on('connect')
def handle_connect(auth):
    room = session.get('room')
    name = session.get('name')
    mode = session.get('mode')
    unique_id = request.sid

    print(f"{name} connected to room {room}")

    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    if len(rooms[room]["participants"]) >= 2:
        # If there are already 2 players in the room, reject the new player's connection
        return redirect(url_for('home_screen'))
    
    join_room(room)
    send({"name": name, "message": "has entered the room."}, to=room)
    rooms[room]["members"] += 1

    if len(rooms[room]["participants"]) == 0 and mode == "multiplayer":
        rooms[room]["participants"].append({
            "player_id": unique_id,
            "name": name,
            "role": "codemaker",
            "guesses": [],
            "winner": False
        })
    else:
        rooms[room]["participants"].append({
            "player_id": unique_id,
            "name": name,
            "role": "codebreaker",
            "guesses": [],
            "winner": False
        })
    print(rooms)

@socketio.on('disconnect')
def handle_disconnect():
    room = session.get('room')
    name = session.get('name')

    leave_room(room)

    send({"name": name, "message": "has left the room."}, to=room)
    print(f"{name} has left room {room}")

@socketio.on('lobby_message')
def handle_lobby_message(data):
    room = session.get('room')
    name = session.get('name')
    
    if room not in rooms:
        return
    
    role = None
    
    for participant in rooms[room]["participants"]:
        if participant["name"] == name:
            role = participant["role"]
            break

    content = {
        "name": name,
        "message": data["data"],
        "role": role
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{name} said: {data['data']}")

@socketio.on('secret_code')
def handle_secret_code(data):
    room = session.get('room')
    name = session.get('name')
    mode = session.get('mode')

    if room not in rooms:
        return
    
    content = {
        "name": name,
        "mode": mode,
        "secret_code": data["code"],
    }

    emit("set_code", content, to=request.sid)
    print(f"{name} set the secret code to {content['secret_code']}")

    chat_message = "The secret code has been set!"
    chat_content = {
        "name": "Server",
        "message": chat_message,
    }
    emit("message", chat_content, to=room)

@socketio.on('multiplayer_guess')
def handle_multiplayer_guess(data):
    room = session.get('room')
    name = session.get('name')
    mode = session.get('mode')
    if mode == 'battle-royale':
        secret_code = rooms[room]["secret_code"]

    if room not in rooms:
        return
    
    content = {
        "name": name,
        "guess": data["guess"],
    }

    if mode == "multiplayer":
        emit("update_guesses", content, to=room)
    else:
        emit("update_guesses", content, to=request.sid)
        guess_feedback = check_guess(secret_code, content['guess'])

        if guess_feedback == "You won! You guessed the code correctly!":
            # update winning player's winner status
            for player in rooms[room]["participants"]:
                if player["player_id"] == request.sid:
                    player["winner"] = True
                    break
            
            print(f"{name} won the battle!")

            emit("guess_feedback", guess_feedback, to=request.sid)
            emit("end_battle", to=room)
        else:
            emit("guess_feedback", guess_feedback, to=request.sid)

    # Append guess to the player's guesses list
    for player in rooms[room]["participants"]:
        if player["player_id"] == request.sid:
            player["guesses"].append(content["guess"])
                
    print(rooms)
    print(f"{name} guessed: {content['guess']}")

    chat_message = f"{name} made their guess!"
    chat_content = {
        "name": "Server",
        "message": chat_message,
    }
    emit("message", chat_content, to=room)

@socketio.on('multiplayer_feedback')
def handle_multiplayer_feedback(data):
    room = session.get('room')
    name = session.get('name')

    if room not in rooms:
        return
    
    content = {
        "name": name,
        "feedback-numbers": data['feedback_numbers'],
        "feedback-locations": data['feedback_locations']
    }

    emit("update_feedback", content, to=room)
    rooms[room]["feedback"] = f"{content['feedback-numbers']} correct numbers, {content['feedback-locations']} correct locations."
    print(rooms)
    print(f"{name} gave feedback: {content['feedback-numbers']} correct numbers, {content['feedback-locations']} correct locations.")

    chat_message = f"{name} provided feedback!"
    chat_content = {
        "name": "Server",
        "message": chat_message,
    }
    emit("message", chat_content, to=room)

def generate_room_code(length):
    """Generate a random 4-character room code."""
    while True:
        code = ""

        for _ in range(length):
            code += choice(ascii_uppercase)

        if code not in rooms:
            break

    return code 

def generate_secret_code():
    """Generate a random 4-digit secret code."""
    
    # code = []

    # for _ in range(4):
    #     code.append(randint(0,7))

    base_url = "https://www.random.org/integers/"

    payload = {'num': 4,
               'min': 0,
               'max': 7,
               'col': 1,
               'base': 10,
               'format': 'plain',
               'rnd': 'new'}

    response = requests.get(base_url, params=payload)

    code = [ int(x) for x in response.text.split('\n')[0:4]]

    print(f"generated: {code}")

    return code

def check_guess(secret_code, guess):
    """Evaluate the player's guess."""
    global game_over, num_attempts, guessed

    # Convert user's guess and secret code into lists
    if not isinstance(guess, list):
        guess = [int(x) for x in guess]
    #TODO: secret code is being converted into a string at some point between the client-server or server-client transmissions.
    # potentially store server-side via as a session variable or as part of the database
    if not isinstance(secret_code, list):
        secret_code = secret_code.strip('][').split(', ')
        secret_code = [int(x) for x in secret_code]

    # Validate the user's guess input
    if len(guess) != 4:
        return "Please enter a 4-digit guess."
    
    for num in guess:
        if num not in [0, 1, 2, 3, 4, 5, 6, 7]:
            return "Please provide only digits between 0 and 7."

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

    print(guess, secret_code)

    secret_code_copy = secret_code.copy()

    # Check for correct numbers 
    for num in guess:
        if num in secret_code_copy:
            correct_numbers += 1
            secret_code_copy.remove(num)

    # Check for correct locations
    for index, num in enumerate(guess):
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

    leaderboard = get_leaderboard()

    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        join = request.form.get('join', False)
        create = request.form.get('create', False)
        mode = request.form.get('mode')

        if not name:
            return render_template('index.html', error="Please enter a name.", code=code, name=name)
        
        if join != False and not code:
            return render_template('index.html', error="Please enter a game code.", code=code, name=name)
        
        room = code

        if create != False:
            if mode == "battle-royale":
                room = 'battle-royale'
                if not rooms:
                    rooms[room] = {"members": 0, "messages": [], "participants": [], "secret_code": generate_secret_code()}
            elif mode == "multiplayer":
                room = generate_room_code(4)
                rooms[room] = {"members": 0, "messages": [], "participants": []}
        elif code not in rooms:
            return render_template('index.html', error="Room does not exist.", code=code, name=name)

        session["room"] = room
        session["name"] = name
        session["mode"] = mode

        # set roles in session
        print(session)

        return redirect(url_for('load_game_room'))
        
    return render_template('index.html', leaderboard=leaderboard)

@app.route('/start_single')
def start_single_game():
    """Start a single-player game."""
    global game_over, num_attempts, guessed

    num_attempts = 10;
    game_over = False;
    guessed = False;

    # Generate a random 4-digit code
    code = generate_secret_code()

    return render_template('game.html', code=code, num_attempts=num_attempts)

@app.route('/game_room')
def load_game_room():
    """Display game room for a multiplayer game."""
    room = session.get("room")
    name = session.get("name")
    mode = session.get("mode")
    
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for('home_screen'))
    
    if len(rooms[room]["participants"]) >= 2:
        print("room full")
        # If there are already 2 players in the room, reject the new player's connection
        return redirect(url_for('home_screen'))

    user_role = None
    if len(rooms[room]["participants"]) == 0 and mode == "multiplayer":
        user_role = 'codemaker'
        print(user_role)
    else:
        user_role = 'codebreaker'
        print(user_role)


    return render_template("multiplayer-game.html", num_attempts=num_attempts, code=room, user_role=user_role, name=name, mode=mode)

@socketio.on('start_game')
def handle_start_game():
    room = session.get("room")
    print(room)
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for('home_screen'))

    emit('update_room', to=room)

@socketio.on('start_battle_royale')
def handle_start_battle_royale():
    global game_over, guessed, num_attempts

    game_over = False;
    guessed = False;
    num_attempts = 10;

    room = session.get("room")
    mode = session.get("mode")
    print(room)
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for('home_screen'))

    emit('update_room', to=room)

    secret_code  = rooms[room]["secret_code"]

    content = {
        "mode": mode,
        "secret_code": secret_code,
    }

    emit('set_code', content, to=room)


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

@app.route('/postgame')
def display_postgame():
    """Display the postgame screen."""
    room = session.get("room")
    name = session.get("name")
    mode = session.get("mode")

    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for('home_screen'))
    
    # collect game data for each player
    game_data = []

    print("Endgame printed: ", name)

    players = rooms[room]["participants"] 

    secret_code = rooms[room]["secret_code"]
    
    for player in players:

        if player['winner'] and player['name'] == name:
            # push player data to database
            player_data = crud.get_user_by_username(player['name'])

            if player_data:
                player_data.total_wins += 1
                crud.update_user_score(player_data)

        game_data.append({
            "name": player['name'],
            "guesses": player['guesses'],
            "winner": player['winner'],
        })
        
    return render_template("postgame.html", mode=mode, secret_code=secret_code, game_data=game_data)

def get_leaderboard():
    """Get database data for leaderboard."""

    top_players = crud.get_top_players()

    print(top_players)

    return top_players

if __name__ == '__main__':
    connect_to_db(app)
    socketio.run(app, debug=True)