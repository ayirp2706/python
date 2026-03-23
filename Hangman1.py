import random

def get_secret_word():
    """Gets the secret word from Player 1."""
    while True:
        word = input("Player 1, enter the secret word (letters only): ").lower()
        if word.isalpha():
            return word
        else:
            print("Invalid input. Please enter letters only.")

def display_hangman(wrong_guesses):
    """Displays the hangman figure based on wrong guesses."""
    stages = [
        # Initial empty gallows
        """
           -----
           |   |
               |
               |
               |
               |
        ---------
        """,
        # Head
        """
           -----
           |   |
           O   |
               |
               |
               |
        ---------
        """,
        # Body
        """
           -----
           |   |
           O   |
           |   |
               |
               |
        ---------
        """,
        # One arm
        """
           -----
           |   |
           O   |
          /|   |
               |
               |
        ---------
        """,
        # Both arms
        """
           -----
           |   |
           O   |
          /|\\  |
               |
               |
        ---------
        """,
        # One leg
        """
           -----
           |   |
           O   |
          /|\\  |
          /    |
               |
        ---------
        """,
        # Both legs - Game Over
        """
           -----
           |   |
           O   |
          /|\\  |
          / \\  |
               |
        ---------
        """
    ]
    print(stages[wrong_guesses])

def play_hangman():
    """Main function to play the two-player Hangman game."""
    secret_word = get_secret_word()
    guessed_letters = []
    wrong_guesses = 0
    max_wrong_guesses = 6

    # Initialize displayed word with underscores
    display_word = ["_" for _ in secret_word]

    print("\n" * 50) # Clear the screen for Player 2 (or just print many newlines)
    print("Welcome to Two-Player Hangman!")

    while wrong_guesses < max_wrong_guesses and "_" in display_word:
        display_hangman(wrong_guesses)
        print(f"Word: {' '.join(display_word)}")
        print(f"Guessed letters: {', '.join(sorted(guessed_letters))}")

        guess = input("Player 2, guess a letter: ").lower()

        if not guess.isalpha() or len(guess) != 1:
            print("Invalid input. Please enter a single letter.")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter. Try again.")
            continue

        guessed_letters.append(guess)

        if guess in secret_word:
            print(f"Good guess! '{guess}' is in the word.")
            for i, char in enumerate(secret_word):
                if char == guess:
                    display_word[i] = guess
        else:
            print(f"Sorry, '{guess}' is not in the word.")
            wrong_guesses += 1

    display_hangman(wrong_guesses) # Show final state of hangman

    if "_" not in display_word:
        print(f"\nCongratulations, Player 2! You guessed the word: '{secret_word}'")
    else:
        print(f"\nGame Over, Player 2! The word was: '{secret_word}'")

if __name__ == "__main__":
    play_hangman()