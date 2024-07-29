#!/usr/bin/python3
"""
Flask web application to display states and their cities.
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """
    Renders a template to display all State objects
    and their linked City objects.
    States and cities are listed in alphabetical order.
    """
    try:
        states = storage.all(State).values()
        sorted_states = sorted(states, key=lambda state: state.name)
        return render_template('8-cities_by_states.html', states=sorted_states)
    except Exception as e:
        app.logger.error(f"Error fetching data: {e}")
        return render_template('8-cities_by_states.html', states=[])


@app.teardown_appcontext
def teardown_db(exception):
    """
    Ensures the current SQLAlchemy session is closed after each request.
    """
    storage.close()
    if exception:
        app.logger.error(f"Teardown error: {exception}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
