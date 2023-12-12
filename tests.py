import unittest
from app import check_guess

class TestCheckGuess(unittest.TestCase):
    
    def test_correct_guess(self):
        secret_code = [1, 2, 3, 4]
        guess = [1, 2, 3]
        result = check_guess(secret_code, guess)
        self.assertEqual(result, "You won! You guessed the code correctly!")
        