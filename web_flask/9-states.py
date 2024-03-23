#!/usr/bin/python3
""" Script that starts a Flask web application """

from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<state_id>', strict_slashes=False)
def show_states(state_id=None):
    """ Display states in alphabetical order """
    states = storage.all("State")
    if state_id is not None:
        state_id = 'State.' + state_id
    return render_template('9-states.html', states=states, state_id=state_id)


@app.teardown_appcontext
def teardown(exception):
    """ Closes the storage """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
