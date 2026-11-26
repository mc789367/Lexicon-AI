import random

from game import MAX_ATTEMPTS, WORDS, Game


def test_new_game_hides_the_word():
    game = Game.new(rng=random.Random(1))
    assert game.word in WORDS
    assert game.attempts_left == MAX_ATTEMPTS
    assert game.guessed == []
    assert game.status == "playing"
    assert set(game.display().split()) == {"_"}
    assert game.word not in game.display()


def test_new_game_uses_the_chooser():
    class Chooser:
        def choice(self, words):
            return words[-1]

    game = Game.new(rng=Chooser())
    assert game.word == WORDS[-1]


def test_hit_reveals_every_copy_and_keeps_attempts():
    game = Game("book")
    kind, message = game.guess("O")
    assert kind == "hit"
    assert message == "o is in the word."
    assert game.display() == "_ o o _"
    assert game.attempts_left == MAX_ATTEMPTS
    assert game.guessed == ["o"]


def test_miss_reduces_attempts():
    game = Game("cat")
    kind, message = game.guess("z")
    assert kind == "miss"
    assert message == "z is not in the word."
    assert game.attempts_left == MAX_ATTEMPTS - 1
    assert game.display() == "_ _ _"


def test_repeat_does_not_change_state():
    game = Game("cat")
    game.guess("c")
    kind, message = game.guess("C")
    assert kind == "repeat"
    assert message == "You already guessed c."
    assert game.guessed == ["c"]
    assert game.attempts_left == MAX_ATTEMPTS
    assert game.status == "playing"


def test_invalid_input_does_not_change_state():
    game = Game("cat")
    for raw in ("", "   ", "1", "!", "ab", "a1"):
        kind, message = game.guess(raw)
        assert kind == "invalid"
        assert message
        assert game.guessed == []
        assert game.attempts_left == MAX_ATTEMPTS
        assert game.status == "playing"


def test_win_stops_further_guesses():
    game = Game("a")
    kind, message = game.guess("a")
    assert kind == "win"
    assert message == "Congratulations, you won."
    assert game.display() == "a"
    assert game.attempts_left == MAX_ATTEMPTS
    kind, message = game.guess("b")
    assert kind == "over"
    assert message == "The game is over."
    assert game.guessed == ["a"]
    assert game.status == "won"


def test_loss_reveals_the_word_and_stops_guesses():
    game = Game("a")
    last = None
    for letter in "bcdefg":
        last = game.guess(letter)
    assert last == ("loss", "Game over. The word was a.")
    assert game.attempts_left == 0
    assert game.status == "lost"
    kind, message = game.guess("a")
    assert kind == "over"
    assert message == "The game is over."
    assert "a" not in game.guessed


def test_restart_resets_state():
    game = Game("house")
    game.guess("z")
    game.guess("h")
    restarted = Game.new(rng=_Fixed("plane"))
    assert restarted.word == "plane"
    assert restarted.attempts_left == MAX_ATTEMPTS
    assert restarted.guessed == []
    assert restarted.status == "playing"


class _Fixed:
    def __init__(self, word):
        self.word = word

    def choice(self, words):
        return self.word
