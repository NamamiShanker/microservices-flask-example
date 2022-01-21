"""Base configuration for the application"""
import os


class BaseConfig:
    """Base configuration"""

    TESTING = False
    DEBUG = False
    FLASK_ENV = "development"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_CONFIG = {
        "broker_url": os.environ.get("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0"),
        "result_backend": os.environ.get("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0"),
        "redis_backend_health_check_interval": 600,
        "imports": ("project.tasks",),
        "worker_send_task_events": True,
    }
