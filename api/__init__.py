import os
from flask import Flask
from flask_socketio import SocketIO
from api.plan_api import PLAN_API

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
    application.register_blueprint(PLAN_API, url_prefix='/v1/plan')

    return application