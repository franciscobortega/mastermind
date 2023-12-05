from random import randint

def generate_code():
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

def main():
    SECRET_CODE = generate_code()
    NUM_ATTEMPTS = 10

    print("Welcome to Mastermind!")
    print(f"You have {NUM_ATTEMPTS} attempts to guess the 4-digit code (0-7). Good luck!", SECRET_CODE) # code visible for debugging

    while NUM_ATTEMPTS != 0:
        guess = input(f"Enter your guess (e.g., 0123): ")

        # convert guess to a list
        guess = [int(x) for x in guess]

        if guess == SECRET_CODE:
            print("You won! You guessed the code correctly!")
            return
        else:
            # evaluate the guess and provide feedback
            feedback = check_guess(SECRET_CODE, guess)
            print(f"Feedback: {feedback}")

        NUM_ATTEMPTS -= 1
    else:
        print(f"Game over! The secret code was: {SECRET_CODE}")

if __name__ == "__main__":
    main()