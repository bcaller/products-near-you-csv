# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask import send_from_directory

from server.api import api


def create_app(settings_overrides=None):
    app = Flask(__name__)
    configure_settings(app, settings_overrides)

    @app.route('/<path:path>')
    def send(path):
        return send_from_directory(app.config['STATIC_PATH'], path)

    configure_blueprints(app)
    return app


def configure_settings(app, settings_override):
    parent = os.path.dirname(__file__)
    data_path = os.path.join(parent, '..', 'data')
    static_path = os.path.join(parent, '..', 'client')
    app.config.update({
        'DEBUG': True,
        'TESTING': False,
        'DATA_PATH': data_path,
        'STATIC_PATH': static_path
    })
    if settings_override:
        app.config.update(settings_override)


def configure_blueprints(app):
    app.register_blueprint(api)
