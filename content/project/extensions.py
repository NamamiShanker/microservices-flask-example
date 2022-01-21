"""Extensions init are done here"""
import time
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .worker import FlaskCeleryExtension

db = SQLAlchemy()
migrate = Migrate()
celery_worker = FlaskCeleryExtension()