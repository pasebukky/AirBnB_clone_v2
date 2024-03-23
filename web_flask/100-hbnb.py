#!/usr/bin/python3
"""A script that starts a web application with two routings """

from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """ Renders states template """
    path = '100-hbnb.html'
    states = storage.all(State)
    amenities = storage.all(Amenity)
    places = storage.all(Place)
    return render_template(path, states=states,
                           amenities=amenities,
                           places=places)


@app.teardown_appcontext
def teardown(exception):
    """ Closes the storage """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
