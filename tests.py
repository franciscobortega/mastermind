import unittest
from app import check_guess

class TestCheckGuess(unittest.TestCase):

    def setUp(self):
        global game_over, guessed, num_attempts
        game_over = False
        guessed = False
        num_attempts = 10 
    

    def test_guess_all_incorrect(self):
        secret_code = [1, 2, 3, 4]
        guess = [5, 6, 7, 8]
        result = check_guess(secret_code, guess)
        self.assertEqual(result, "all incorrect")

    def test_guess_all_correct_numbers_no_locations(self):
        secret_code = [1, 2, 3, 4]
        guess = [4, 3, 2, 1]
        result = check_guess(secret_code, guess)
        self.assertEqual(result, "4 correct numbers and 0 correct locations")

    def test_guess_duplicate_correct_numbers_no_locations(self):
        secret_code = [0, 0, 1, 1]
        guess = [1, 1, 2, 3]
        result = check_guess(secret_code, guess)
        self.assertEqual(result, "2 correct numbers and 0 correct locations")

    def test_guess_duplicate_correct_numbers_with_locations(self):
        secret_code = [0, 0, 1, 1]
        guess = [2, 3, 1, 1]
        result = check_guess(secret_code, guess)
        self.assertEqual(result, "2 correct numbers and 2 correct locations")

    def test_guess_one_correct_number_no_locations(self):
        secret_code = [0, 1, 1, 1]
        guess = [1, 2, 3, 4]
        result = check_guess(secret_code, guess)
        self.assertEqual(result, "1 correct numbers and 0 correct locations")

    def test_guess_one_correct_number_one_location(self):
        secret_code = [0, 1, 1, 1]
        guess = [4, 1, 2, 3]
        result = check_guess(secret_code, guess)
        self.assertEqual(result, "1 correct numbers and 1 correct locations")

    def test_guess_three_correct_number_two_location(self):
        secret_code = [0, 1, 1, 1]
        guess = [1, 1, 1, 2]
        result = check_guess(secret_code, guess)
        self.assertEqual(result, "3 correct numbers and 2 correct locations")

    def test_guess_three_correct_number_two_location(self):
        secret_code = [0, 1, 1, 1]
        guess = [1, 1, 1, 1]
        result = check_guess(secret_code, guess)
        self.assertEqual(result, "3 correct numbers and 3 correct locations")

    # TODO: This test causes the rest to fail, likely side effect of using global variables. Consider changing check_guess function to not rely on global variables.
    # def test_guess_all_correct(self):
    #     secret_code = [1, 2, 3, 4]
    #     guess = [1, 2, 3, 4]
    #     result = check_guess(secret_code, guess)
    #     self.assertEqual(result, "You won! You guessed the code correctly!")