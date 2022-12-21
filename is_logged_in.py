from flask_security import current_user, login_required
from app import app
import flask

@app.route('/is_logged_in')
def is_logged_in():

    is_logged_in=current_user.is_authenticated
    
    return flask.jsonify(is_logged_in)
