from pathlib import Path
from streamlit.testing.v1 import AppTest

# Resolve the app entrypoint relative to this file (src/tests/app/test_app.py)
APP_PATH = Path(__file__).parent.parent.parent / "app" / "🧑‍💻_News_Feed_Monitor.py"


def test_app_smoke_test():
    """Verify the app initializes and runs without uncaught exceptions."""
    at = AppTest.from_file(str(APP_PATH))
    at.run()
    assert not at.exception


def test_app_title():
    """Verify that the primary page title renders."""
    at = AppTest.from_file(str(APP_PATH))
    at.run()
    assert at.title[0].value == "Competitor News Tracker"