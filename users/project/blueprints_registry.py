"""All the blueprints are registered over here"""
from flask import Flask

def register_blueprints(app):
	"""Register all the blueprints here"""

	from project.api.users import users_blueprint
	app.register_blueprint(users_blueprint, url_prefix='/user_api')

	return