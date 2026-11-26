"""Single-player word guessing game."""

import streamlit as st

from game import Game

st.set_page_config(page_title="Word Guessing Game")
st.title("Word Guessing Game")

if "game" not in st.session_state:
    st.session_state.game = Game.new()
    st.session_state.feedback = None

if st.button("New game"):
    st.session_state.game = Game.new()
    st.session_state.feedback = None

game = st.session_state.game

if game.status == "playing":
    with st.form("guess", clear_on_submit=True):
        letter = st.text_input("Guess a letter")
        submitted = st.form_submit_button("Guess")
    if submitted:
        kind, message = game.guess(letter)
        st.session_state.feedback = (kind, message)

st.text(game.display())
st.write(f"Incorrect attempts remaining: {game.attempts_left}")
guessed = ", ".join(game.guessed) if game.guessed else "None"
st.write(f"Letters guessed: {guessed}")

feedback = st.session_state.feedback
if feedback:
    kind, message = feedback
    if kind in ("hit", "win"):
        st.success(message)
    elif kind in ("miss", "loss"):
        st.error(message)
    else:
        st.warning(message)
