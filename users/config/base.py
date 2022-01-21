"""Base configuration for the application"""
import os

class BaseConfig:
	"""Base configuration"""
	TESTING = False
	DEBUG = False
	FLASK_ENV = 'development'
	SQLALCHEMY_TRACK_MODIFICATIONS = False