from abc import ABC
from flask import Flask
from celery import Task, current_app as current_celery_app


def make_celery(flask_app: Flask):
    celery = current_celery_app

    celery.config_from_object(
        flask_app.import_name,
    )
    celery.conf.update(flask_app.config.get("CELERY_CONFIG"))

    celery.Task = AppContextTask

    # Set Flask application object on the Celery application.
    if not hasattr(celery, "flask_app"):
        celery.flask_app = flask_app

    return celery


class AppContextTask(Task, ABC):
    """Celery task running within a Flask application context.
    Expects the associated Flask application to be set on the bound
    Celery application.
    """

    abstract = True

    def __call__(self, *args, **kwargs):
        """Execute task."""
        with self.app.flask_app.app_context():
            return Task.__call__(self, *args, **kwargs)


class FlaskCeleryExtension(object):
    """Flask-Celery extension."""

    def __init__(self, app: Flask = None, create_celery_app=make_celery):
        """Initialize the Flask Celery Extension."""
        self.create_celery_app = create_celery_app
        self.celery = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        """Initialize a Flask application."""
        self.celery = self.create_celery_app(app)
