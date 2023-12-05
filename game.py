import random

def generate_code():
    return [1,2,3,4]

def check_guess(secret_code, guess):
    pass

def main():
    SECRET_CODE = generate_code()
    NUM_ATTEMPTS = 10

    print("Welcome to Mastermind!")
    print(f"You have {NUM_ATTEMPTS} attempts to guess the 4-digit code (0-7). Good luck!", SECRET_CODE) # code visible for debugging

    if NUM_ATTEMPTS != 0:
        guess = input(f"Enter your guess (e.g., 0123): ")

        # convert guess to a list
        guess = [int(x) for x in guess]

        if guess == SECRET_CODE:
            print("You won! You guessed the code correctly!")
            return
        
        # evaluate the guess and provide feedback
        feedback = check_guess(SECRET_CODE, guess)
        print(f"Feedback: {feedback}")

    else:
        print(f"Game over! The secret code was: {SECRET_CODE}")

if __name__ == "__main__":
    main()