import os
from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app():
    """Create an application."""
    application = Flask(__name__)
    application.config.update({
        'DEBUG': True,
        'SECRET_KEY': '711e1f0fdded4ea7bf5d6702897b3b40'
    })

    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
    socketio.init_app(application)

    # register blueprint to app
    # application.register_blueprint(USER_API, url_prefix='/v1/user')
    # application.register_blueprint(BOOK_API, url_prefix='/mybooks')

    return application