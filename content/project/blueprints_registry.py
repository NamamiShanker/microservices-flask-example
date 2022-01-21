"""All the blueprints are registered over here"""
from flask import Flask


def register_blueprints(app):
    """Register all the blueprints here"""

    from project.api.content import contents_blueprint

    app.register_blueprint(contents_blueprint, url_prefix="/content_api")

    return
