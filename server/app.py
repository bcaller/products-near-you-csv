# -*- coding: utf-8 -*-

import os

from flask import Flask
from flask import g
from flask import send_from_directory

import server
from server.shop_data import ShopData
from server.api import api

from server.flask_extensions import EnhancedFloatConverter, extend_json


def create_app(settings_overrides=None):
    app = Flask(__name__)
    app.json_encoder = extend_json(app.json_encoder)
    configure_settings(app, settings_overrides)
    configure_static_files(app)
    app.url_map.converters['float'] = EnhancedFloatConverter
    configure_blueprints(app)
    with app.app_context():
        app.data = ShopData(server.api.data_path)
    return app


def configure_static_files(app):
    @app.route('/')
    @app.route('/<path:path>')
    def static_files(path='index.html'):
        return send_from_directory(app.config['STATIC_PATH'], path)


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
