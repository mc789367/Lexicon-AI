# Handoff — Word Guessing Game v1 (MVP)

## What was done

- Reviewed the repo. The only existing file is `CLAUDE.md`. There is no application code, virtual environment, dependency file, or tests.
- Read `CLAUDE.md`. It points at the Karpathy behavioral guidelines: state assumptions, keep the solution minimal, change only what the task needs, and define checks that can be verified.
- Wrote this handoff. The game is not implemented yet.

## What this feature is

A single-player word guessing game in a Python Streamlit app, close to Hangman. One hidden English word, letter guesses, six wrong attempts. No accounts, saved scores, database, difficulty levels, or multiplayer.

## Game behavior

- Start and restart pick a new random word from a fixed list and reset guesses and attempts.
- The word stays hidden. Unguessed letters show as underscores.
- The screen shows remaining incorrect attempts and letters already guessed.
- One letter per guess. Matching letters reveal in every position, with positive feedback. A miss costs one attempt, with negative feedback.
- A game starts with six incorrect attempts. Correct guesses do not cost an attempt. A repeated letter does not cost an attempt and does not change the board.
- Input is one English letter, A–Z, case-insensitive. Empty input, numbers, symbols, and multi-character input are rejected with a clear message and do not change state.
- Win: every letter is revealed. Show a congratulatory message and stop accepting guesses.
- Loss: attempts reach zero. Show a game-over message, reveal the word, and stop accepting guesses.

## Assumptions for the next agent

- Keep rules in plain Python, separate from Streamlit, so pytest can run them without the UI.
- Keep a small predefined word list in the repo. No network word source.
- Store the current game in Streamlit session state.
- Compare and store letters in lowercase.
- Positive and negative feedback are Streamlit success and error messages.
- A correct guess that finishes the word is a win. A miss that hits zero attempts is a loss. Those two cannot happen on the same guess.

## Suggested layout

- `game.py` — word selection, guesses, win, and loss
- `app.py` — Streamlit UI
- `tests/test_game.py` — pytest for the rules above
- `requirements.txt` — `streamlit` and `pytest`
- A local virtual environment for those packages

## Checks the implementation should pass

- New game hides the word, starts at six attempts, and has no guessed letters.
- A hit reveals every copy of that letter and leaves attempts unchanged.
- A miss reduces attempts by one.
- Repeat guesses and invalid input leave state unchanged and explain why.
- Win and loss stop further guesses.
- Restart replaces the word and clears guesses and attempts.

## Out of scope

User authentication, persistent scores, MongoDB, difficulty levels, and multiplayer.
