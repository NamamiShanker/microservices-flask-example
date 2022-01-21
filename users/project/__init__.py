"""The application factory and the application main hub begins from here"""
import os

from flask import Flask

from .blueprints_registry import register_blueprints
from .extensions import db, migrate

def create_app():

	app = Flask(__name__)
	
	app_settings = os.getenv('APP_SETTINGS')
	app.config.from_object(app_settings)

	register_models()
	add_extensions(app)
	register_blueprints(app)
	error_handler_registry(app)

	@app.shell_context_processor
	def ctx():
		return {'app': app, 'db': db}
	
	return app

def add_extensions(app):
	db.init_app(app)
	migrate.init_app(app, db)

def register_models():
	"""Register Models, so as the migration scrip recognises in order to create the tables"""
	from project.api.users import UserDB

	return

def error_handler_registry(app: Flask):
    """Register functions with application
    :param app: Flask Instance
    :return None
    """
    from project.lib.errors import (
        BadRequest,
        ServerError,
        bad_request_handler,
        server_error_handler,
    )

    app.register_error_handler(BadRequest, bad_request_handler)
    app.register_error_handler(ServerError, server_error_handler)

    return None
