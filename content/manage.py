from flask.cli import FlaskGroup

from project import create_app, celery_worker

app = create_app()
cli = FlaskGroup(create_app=create_app)
celery = celery_worker.celery

if __name__ == "__main__":
    cli()
