from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_logged_out_user_cannot_access_the_game():
    app_path = Path(__file__).parents[1] / "app.py"
    app = AppTest.from_file(str(app_path)).run()

    assert not app.exception
    assert [field.label for field in app.text_input] == ["Username", "Password"]
