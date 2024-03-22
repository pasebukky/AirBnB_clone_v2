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
def flask_text(text):
    """ Displays “C ” followed by the value of the text variable """
    text = text.replace("_", " ")
    return "C {}".format(text)


@app.route("/python/", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def flask_python(text="is cool"):
    """ Displays “Python ”, followed by the value of the text variable """
    text = text.replace("_", " ")
    return "Python {}".format(text)


@app.route("/number/<n>", strict_slashes=False)
def flask_number(n):
    """ Displays “n is a number” only if n is an integer """
    return "{} is a number".format(n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
