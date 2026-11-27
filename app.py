"""Single-player word guessing game."""

import streamlit as st
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from auth import authenticate_user, register_user
from game import Game

st.set_page_config(page_title="Word Guessing Game")
st.title("Word Guessing Game")


@st.cache_resource
def get_users_collection():
    settings = st.secrets["mongo"]
    client = MongoClient(settings["uri"], serverSelectionTimeoutMS=5000)
    users = client[settings["database"]]["users"]
    users.create_index("username", unique=True)
    users.create_index("email", unique=True)
    return users


if "username" not in st.session_state:
    page = st.radio("Account", ("Log in", "Sign up"), horizontal=True)
    if page == "Sign up":
        st.subheader("Create an account")
        with st.form("signup"):
            username = st.text_input("Username")
            email = st.text_input("Email address")
            password = st.text_input("Password", type="password")
            confirmation = st.text_input("Confirm password", type="password")
            submitted = st.form_submit_button("Sign up")
        if submitted:
            if password != confirmation:
                st.error("Passwords do not match.")
            else:
                try:
                    success, message = register_user(
                        get_users_collection(), username, email, password
                    )
                except PyMongoError:
                    st.error("Unable to reach the account service. Please try again.")
                else:
                    (st.success if success else st.error)(message)
    else:
        st.subheader("Log in")
        with st.form("login"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Log in")
        if submitted:
            try:
                logged_in_username = authenticate_user(
                    get_users_collection(), username, password
                )
            except PyMongoError:
                st.error("Unable to reach the account service. Please try again.")
            else:
                if logged_in_username:
                    st.session_state["username"] = logged_in_username
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
    st.stop()

st.sidebar.text(f"Logged in as: {st.session_state['username']}")
if st.sidebar.button("Log out"):
    st.session_state.pop("username", None)
    st.session_state.pop("game", None)
    st.session_state.pop("feedback", None)
    st.rerun()

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
