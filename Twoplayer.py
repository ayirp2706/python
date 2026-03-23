import tkinter as tk
from tkinter import messagebox
import pygame

# Initialize pygame for sound
pygame.mixer.init()

# Load sounds (make sure these files exist in your folder)
correct_sound = "correct.wav"
wrong_sound = "wrong.wav"
win_sound = "win.wav"
lose_sound = "lose.wav"

# Function to play sound
def play_sound(sound_file):
    try:
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
    except Exception as e:
        print("Sound error:", e)

# Hangman stages
HANGMAN_PICS = [
    "-----\n|   |\n    |\n    |\n    |\n    |\n---------",
    "-----\n|   |\nO   |\n    |\n    |\n    |\n---------",
    "-----\n|   |\nO   |\n|   |\n    |\n    |\n---------",
    "-----\n|   |\nO   |\n/|  |\n    |\n    |\n---------",
    "-----\n|   |\nO   |\n/|\\ |\n    |\n    |\n---------",
    "-----\n|   |\nO   |\n/|\\ |\n/   |\n    |\n---------",
    "-----\n|   |\nO   |\n/|\\ |\n/ \\ |\n    |\n---------",
]

class TwoPlayerHangman:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Two Player Hangman (Tkinter + Sound)")
        self.root.geometry("520x600")
        self.root.configure(bg="#fafafa")

        self.secret_word = ""
        self.hint = ""
        self.guessed_letters = []
        self.wrong_guesses = 0
        self.max_wrong_guesses = 6

        # --- Screen 1: Player 1 Setup ---
        self.setup_frame = tk.Frame(root, bg="#fafafa")
        self.setup_frame.pack(pady=20)

        tk.Label(self.setup_frame, text="👤 Player 1: Enter the Secret Word", font=("Arial", 14, "bold"), bg="#fafafa").pack(pady=5)
        self.secret_entry = tk.Entry(self.setup_frame, font=("Arial", 14), show="*", width=20, justify="center")
        self.secret_entry.pack(pady=5)

        tk.Label(self.setup_frame, text="💡 Enter a Hint for Player 2", font=("Arial", 14), bg="#fafafa").pack(pady=5)
        self.hint_entry = tk.Entry(self.setup_frame, font=("Arial", 14), width=25, justify="center")
        self.hint_entry.pack(pady=5)

        tk.Button(self.setup_frame, text="Start Game", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=15,
                  command=self.start_game).pack(pady=15)

    def start_game(self):
        self.secret_word = self.secret_entry.get().lower()
        self.hint = self.hint_entry.get()
        if not self.secret_word.isalpha():
            messagebox.showwarning("Invalid", "Secret word must contain only letters.")
            return
        if not self.hint.strip():
            messagebox.showwarning("Invalid", "Please enter a hint.")
            return

        self.display_word = ["_" for _ in self.secret_word]
        self.guessed_letters = []
        self.wrong_guesses = 0

        self.setup_frame.destroy()
        self.create_game_ui()

    def create_game_ui(self):
        # --- Screen 2: Player 2 Gameplay ---
        self.title_label = tk.Label(self.root, text="🎮 Player 2: Guess the Word!", font=("Arial", 20, "bold"), bg="#fafafa")
        self.title_label.pack(pady=10)

        self.hint_label = tk.Label(self.root, text=f"💡 Hint: {self.hint}", font=("Arial", 14, "italic"), bg="#fafafa", fg="#333")
        self.hint_label.pack(pady=5)

        self.word_label = tk.Label(self.root, text=" ".join(self.display_word), font=("Consolas", 24), bg="#fafafa")
        self.word_label.pack(pady=20)

        input_frame = tk.Frame(self.root, bg="#fafafa")
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Enter a letter:", font=("Arial", 12), bg="#fafafa").grid(row=0, column=0, padx=5)
        self.guess_entry = tk.Entry(input_frame, font=("Arial", 14), width=8, justify="center")
        self.guess_entry.grid(row=0, column=1, padx=5)

        self.guess_button = tk.Button(input_frame, text="Guess", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                                      width=10, command=self.make_guess)
        self.guess_button.grid(row=0, column=2, padx=5)

        self.hangman_label = tk.Label(self.root, text=HANGMAN_PICS[0], font=("Consolas", 12), bg="#fafafa")
        self.hangman_label.pack(pady=20)

        self.guessed_label = tk.Label(self.root, text="Guessed: None", font=("Arial", 12), bg="#fafafa")
        self.guessed_label.pack(pady=10)

        self.reset_button = tk.Button(self.root, text="🔁 Restart", font=("Arial", 12, "bold"), bg="#2196F3", fg="white",
                                      width=12, command=self.restart_game)
        self.reset_button.pack(pady=10)

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
            messagebox.showinfo("🎉 Player 2 Wins!", f"Correct! The word was '{self.secret_word}'")
            self.ask_restart()
        elif self.wrong_guesses >= self.max_wrong_guesses:
            play_sound(lose_sound)
            messagebox.showerror("💀 Player 2 Lost!", f"Out of guesses! The word was '{self.secret_word}'")
            self.ask_restart()

    def ask_restart(self):
        if messagebox.askyesno("Play Again?", "Start a new two-player game?"):
            self.root.destroy()
            main()
        else:
            self.root.destroy()

    def restart_game(self):
        self.root.destroy()
        main()

# Run game
def main():
    root = tk.Tk()
    game = TwoPlayerHangman(root)
    root.mainloop()

if __name__ == "__main__":
    main()
