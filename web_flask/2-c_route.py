#!/usr/bin/python3
""" Script that starts a Flask web application """

from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def flask_hello():
    """ Display a specific text """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def flask_hbnb():
    """ Displays a specific text """
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def flask_text():
    """ Displays “C ” followed by the value of the text variable """
    return "C" + text.replace("_", " ")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
