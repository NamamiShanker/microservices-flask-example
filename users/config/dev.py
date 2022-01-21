import os

from . import BaseConfig

class DevelopmentConfig(BaseConfig):
	"""Development configuration"""
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')