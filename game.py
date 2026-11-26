"""Word guessing rules, separate from the Streamlit screen."""

import random

WORDS = (
    "apple",
    "river",
    "plane",
    "stone",
    "light",
    "bread",
    "crane",
    "house",
)

MAX_ATTEMPTS = 6
_LETTERS = set("abcdefghijklmnopqrstuvwxyz")


class Game:
    def __init__(self, word):
        self.word = word.lower()
        self.attempts_left = MAX_ATTEMPTS
        self.guessed = []
        self.status = "playing"

    @classmethod
    def new(cls, rng=None, words=WORDS):
        chooser = rng if rng is not None else random
        return cls(chooser.choice(words))

    def display(self):
        return " ".join(letter if letter in self.guessed else "_" for letter in self.word)

    def guess(self, raw):
        if self.status != "playing":
            return "over", "The game is over."

        if raw is None or not raw.strip():
            return "invalid", "Enter a letter."

        letter = raw.strip()
        if len(letter) != 1 or letter.lower() not in _LETTERS:
            return "invalid", "Enter a single letter from A to Z."

        letter = letter.lower()
        if letter in self.guessed:
            return "repeat", f"You already guessed {letter}."

        self.guessed.append(letter)
        if letter in self.word:
            if all(character in self.guessed for character in self.word):
                self.status = "won"
                return "win", "Congratulations, you won."
            return "hit", f"{letter} is in the word."

        self.attempts_left -= 1
        if self.attempts_left == 0:
            self.status = "lost"
            return "loss", f"Game over. The word was {self.word}."
        return "miss", f"{letter} is not in the word."
