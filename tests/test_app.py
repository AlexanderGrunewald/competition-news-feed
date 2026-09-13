from streamlit.testing.v1 import AppTest


def test_app_smoke_test():
    """Initializes the app and verifies it boots without raising exceptions."""
    # Replace 'app.py' with your Streamlit entrypoint file
    at = AppTest.from_file("app.py")
    at.run()

    # Asserts that no uncaught exceptions occurred during script execution
    assert not at.exception


def test_app_title():
    """Verifies that the main title renders correctly."""
    at = AppTest.from_file("app.py")
    at.run()

    # Checks the first rendered title on the page
    assert at.title[0].value == "Competitor News Tracker"