from flask import jsonify
from werkzeug.exceptions import HTTPException
import traceback
from constants.error_lib import BackEndException
from api import create_app, socketio

application = create_app()

@application.route('/', methods=['GET'])
def home():
    return 'Welcome'


@application.errorhandler(BackEndException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@application.errorhandler(Exception)
def handle_error(e):
    print('handling error')
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    print(traceback.format_exc())

    return jsonify(error='Internal Server Error'), code


if __name__ == "__main__":
    socketio.run(application, host='0.0.0.0', debug=True, port=8080)
