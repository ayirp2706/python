import random

def hangman():
    words = ["python", "programming", "computer", "challenge", "keyboard", "developer", "algorithm"]
    chosen_word = random.choice(words).lower()
    guessed_letters = []
    incorrect_guesses = 0
    max_incorrect_guesses = 6

    print("Welcome to Hangman!")
    print("Try to guess the word.")

    while incorrect_guesses < max_incorrect_guesses:
        display_word = ""
        for letter in chosen_word:
            if letter in guessed_letters:
                display_word += letter
            else:
                display_word += "_"
        print(f"\nWord: {display_word}")
        print(f"Incorrect guesses remaining: {max_incorrect_guesses - incorrect_guesses}")
        print(f"Guessed letters: {', '.join(sorted(guessed_letters))}")

        if "_" not in display_word:
            print("\nCongratulations! You guessed the word correctly!")
            break

        guess = input("Guess a letter: ").lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Invalid input. Please enter a single letter.")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter. Try again.")
            continue

        guessed_letters.append(guess)

        if guess in chosen_word:
            print(f"Good guess! '{guess}' is in the word.")
        else:
            print(f"Sorry, '{guess}' is not in the word.")
            incorrect_guesses += 1

    if incorrect_guesses == max_incorrect_guesses:
        print("\nGame Over! You ran out of guesses.")
        print(f"The word was: {chosen_word}")

if __name__ == "__main__":
    hangman()