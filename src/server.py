""" Module Imports """
import markdown
from flask import Flask

""" Flask App Object """
APP = Flask(__name__)


@APP.route("/")
def home():
    """Serve README on index page as HTML"""
    with open("README.md") as f:
        readme_contents = f.read()
    return markdown.markdown(readme_contents)


def start_flask_server():
    """Starts the Flask server"""
    APP.run(host="0.0.0.0")
