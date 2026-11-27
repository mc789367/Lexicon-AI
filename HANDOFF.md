# Handoff — Word Guessing Game v1 (MVP)

## What was done

- Implemented the word guessing game and its tests.
- Added username/email/password registration and username/password login backed by MongoDB Atlas.
- Passwords are stored as PBKDF2 hashes with per-user random salts.
- The game is available only after login; the app displays the logged-in username and provides logout.

## What this feature is

A single-player word guessing game in a Python Streamlit app, close to Hangman. One hidden English word, letter guesses, six wrong attempts. Accounts are stored in MongoDB Atlas; saved scores, difficulty levels, and multiplayer are not included.

## MongoDB setup

Add a `.streamlit/secrets.toml` file locally (it is git-ignored):

```toml
[mongo]
uri = "mongodb+srv://..."
database = "language_learning"
```

The app creates unique indexes for usernames and email addresses. Never commit the secrets file or put credentials in source code.

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
- `auth.py` — password hashing, registration, and credential verification
- `app.py` — Streamlit UI and login/session handling
- `tests/test_game.py` — pytest for the rules above
- `tests/test_auth.py` — pytest for account behavior
- `requirements.txt` — Streamlit, PyMongo, and pytest
- A local virtual environment for those packages

## Checks the implementation should pass

- New game hides the word, starts at six attempts, and has no guessed letters.
- A hit reveals every copy of that letter and leaves attempts unchanged.
- A miss reduces attempts by one.
- Repeat guesses and invalid input leave state unchanged and explain why.
- Win and loss stop further guesses.
- Restart replaces the word and clears guesses and attempts.
- Registration hashes the password, rejects duplicates, and allows successful login.
- Failed login is rejected; logged-out users cannot access the game.

## Out of scope

Persistent scores, difficulty levels, and multiplayer.
