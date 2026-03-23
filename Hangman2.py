
import tkinter as tk
from tkinter import messagebox
import random
import pygame

# Initialize pygame for sound
pygame.mixer.init()

# Load sounds (you can use your own .wav or .mp3 files)
correct_sound = "correct.wav"
wrong_sound = "wrong.wav"
win_sound = "win.wav"
lose_sound = "lose.wav"

# Function to play a sound safely
def play_sound(sound_file):
    try:
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
    except Exception as e:
        print("Sound error:", e)

# Word list for single player
WORDS = ["python", "hangman", "developer", "frontend", "backend", "data", "science", "machine", "learning"]

# Hangman stages as text art (optional, just for reference)
HANGMAN_PICS = [
    "-----\n|   |\n    |\n    |\n    |\n    |\n---------",
    "-----\n|   |\nO   |\n    |\n    |\n    |\n---------",
    "-----\n|   |\nO   |\n|   |\n    |\n    |\n---------",
    "-----\n|   |\nO   |\n/|  |\n    |\n    |\n---------",
    "-----\n|   |\nO   |\n/|\\ |\n    |\n    |\n---------",
    "-----\n|   |\nO   |\n/|\\ |\n/   |\n    |\n---------",
    "-----\n|   |\nO   |\n/|\\ |\n/ \\ |\n    |\n---------",
]

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Hangman Game (Tkinter + Sound)")
        self.root.geometry("500x500")
        self.root.configure(bg="#fafafa")

        self.secret_word = random.choice(WORDS)
        self.guessed_letters = []
        self.wrong_guesses = 0
        self.max_wrong_guesses = 6

        self.display_word = ["_" for _ in self.secret_word]

        # Title Label
        self.title_label = tk.Label(root, text="🎯 Hangman Game", font=("Arial", 20, "bold"), bg="#fafafa")
        self.title_label.pack(pady=10)

        # Display Word Label
        self.word_label = tk.Label(root, text=" ".join(self.display_word), font=("Consolas", 24), bg="#fafafa")
        self.word_label.pack(pady=20)

        # Entry for letter input
        self.input_label = tk.Label(root, text="Enter a letter:", font=("Arial", 12), bg="#fafafa")
        self.input_label.pack()
        self.guess_entry = tk.Entry(root, font=("Arial", 14), justify="center")
        self.guess_entry.pack(pady=5)

        # Guess Button
        self.guess_button = tk.Button(root, text="Guess", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                                      command=self.make_guess)
        self.guess_button.pack(pady=10)

        # Hangman Label (Text art)
        self.hangman_label = tk.Label(root, text=HANGMAN_PICS[0], font=("Consolas", 12), bg="#fafafa")
        self.hangman_label.pack(pady=10)

        # Guessed Letters
        self.guessed_label = tk.Label(root, text="Guessed: None", font=("Arial", 12), bg="#fafafa")
        self.guessed_label.pack(pady=10)

        # Reset Button
        self.reset_button = tk.Button(root, text="Restart Game", font=("Arial", 12, "bold"), bg="#2196F3", fg="white",
                                      command=self.reset_game)
        self.reset_button.pack(pady=15)

    def make_guess(self):
        guess = self.guess_entry.get().lower()
        self.guess_entry.delete(0, tk.END)

        if not guess.isalpha() or len(guess) != 1:
            messagebox.showwarning("Invalid", "Please enter a single letter.")
            return

        if guess in self.guessed_letters:
            messagebox.showinfo("Already Guessed", f"You already guessed '{guess}'.")
            return

        self.guessed_letters.append(guess)
        self.guessed_label.config(text="Guessed: " + ", ".join(sorted(self.guessed_letters)))

        if guess in self.secret_word:
            play_sound(correct_sound)
            for i, char in enumerate(self.secret_word):
                if char == guess:
                    self.display_word[i] = guess
            self.word_label.config(text=" ".join(self.display_word))
        else:
            play_sound(wrong_sound)
            self.wrong_guesses += 1
            self.hangman_label.config(text=HANGMAN_PICS[self.wrong_guesses])

        if "_" not in self.display_word:
            play_sound(win_sound)
            messagebox.showinfo("🎉 You Win!", f"Congratulations! You guessed '{self.secret_word}'")
            self.ask_restart()
        elif self.wrong_guesses >= self.max_wrong_guesses:
            play_sound(lose_sound)
            messagebox.showerror("💀 Game Over", f"You lost! The word was '{self.secret_word}'")
            self.ask_restart()

    def ask_restart(self):
        if messagebox.askyesno("Play Again?", "Do you want to play another round?"):
            self.reset_game()
        else:
            self.root.destroy()

    def reset_game(self):
        self.secret_word = random.choice(WORDS)
        self.guessed_letters = []
        self.wrong_guesses = 0
        self.display_word = ["_" for _ in self.secret_word]

        self.word_label.config(text=" ".join(self.display_word))
        self.hangman_label.config(text=HANGMAN_PICS[0])
        self.guessed_label.config(text="Guessed: None")

# Run Game
if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()

# second code
# import pygame
# import sys

# # Initialize pygame
# pygame.init()

# # Set up screen
# WIDTH, HEIGHT = 800, 600
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Two Player Word Guess Game")

# # Colors
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)

# # Fonts
# font = pygame.font.Font(None, 48)
# small_font = pygame.font.Font(None, 36)

# # Player 1 input (in console)
# secret_word = input("Player 1: Enter a secret word: ").upper()
# hint = input("Enter a hint for Player 2: ")

# # Hide the word
# guessed = ["_"] * len(secret_word)
# attempts = 6
# guessed_letters = []

# # --- Optional sounds (if you have them) ---
# try:
#     correct_sound = pygame.mixer.Sound("correct.wav")
#     wrong_sound = pygame.mixer.Sound("wrong.wav")
#     win_sound = pygame.mixer.Sound("win.wav")
#     lose_sound = pygame.mixer.Sound("lose.wav")
# except:
#     correct_sound = wrong_sound = win_sound = lose_sound = None

# # Game loop
# running = True
# while running:
#     screen.fill(WHITE)

#     # Display word progress
#     word_display = font.render(" ".join(guessed), True, BLACK)
#     screen.blit(word_display, (100, 200))

#     # Display hint
#     hint_text = small_font.render(f"Hint: {hint}", True, BLACK)
#     screen.blit(hint_text, (100, 100))

#     # Display attempts left
#     attempt_text = small_font.render(f"Attempts left: {attempts}", True, BLACK)
#     screen.blit(attempt_text, (100, 300))

#     # Display guessed letters
#     letters_text = small_font.render("Guessed: " + ", ".join(guessed_letters), True, BLACK)
#     screen.blit(letters_text, (100, 350))

#     pygame.display.flip()

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#         elif event.type == pygame.KEYDOWN:
#             if event.unicode.isalpha():
#                 letter = event.unicode.upper()

#                 if letter not in guessed_letters:
#                     guessed_letters.append(letter)

#                     if letter in secret_word:
#                         for i, ch in enumerate(secret_word):
#                             if ch == letter:
#                                 guessed[i] = letter
#                         if correct_sound:
#                             correct_sound.play()
#                     else:
#                         attempts -= 1
#                         if wrong_sound:
#                             wrong_sound.play()

#     # Check win or lose
#     if "_" not in guessed:
#         screen.fill(WHITE)
#         win_text = font.render("You Win! 🎉", True, (0, 128, 0))
#         screen.blit(win_text, (300, 250))
#         pygame.display.flip()
#         if win_sound:
#             win_sound.play()
#         pygame.time.wait(3000)
#         running = False

#     elif attempts == 0:
#         screen.fill(WHITE)
#         lose_text = font.render(f"You Lose! Word: {secret_word}", True, (255, 0, 0))
#         screen.blit(lose_text, (150, 250))
#         pygame.display.flip()
#         if lose_sound:
#             lose_sound.play()
#         pygame.time.wait(3000)
#         running = False

# pygame.quit()
# sys.exit()
