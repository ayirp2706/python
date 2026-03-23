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

# Hangman stages as text art
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
        self.root.geometry("500x550")
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

        # Entry + Guess Button Frame
        input_frame = tk.Frame(root, bg="#fafafa")
        input_frame.pack(pady=5)

        self.input_label = tk.Label(input_frame, text="Enter a letter:", font=("Arial", 12), bg="#fafafa")
        self.input_label.grid(row=0, column=0, padx=5)

        self.guess_entry = tk.Entry(input_frame, font=("Arial", 14), justify="center", width=8)
        self.guess_entry.grid(row=0, column=1, padx=5)

        self.guess_button = tk.Button(input_frame, text="Guess", font=("Arial", 12, "bold"),
                                      bg="#4CAF50", fg="white", width=12, height=1,
                                      command=self.make_guess)
        self.guess_button.grid(row=0, column=2, padx=5)

        # Hangman Label (ASCII art)
        self.hangman_label = tk.Label(root, text=HANGMAN_PICS[0], font=("Consolas", 12), bg="#fafafa")
        self.hangman_label.pack(pady=20)

        # Guessed Letters
        self.guessed_label = tk.Label(root, text="Guessed: None", font=("Arial", 12), bg="#fafafa")
        self.guessed_label.pack(pady=10)

        # Restart Button (centered and larger)
        self.reset_button = tk.Button(root, text="🔁 Restart Game", font=("Arial", 12, "bold"),
                                      bg="#2196F3", fg="white", width=15, height=1,
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
