"""All the blueprints are registered over here"""
from flask import Flask


def register_blueprints(app):
    """Register all the blueprints here"""
    from project.api.reads import reads_blueprint
    app.register_blueprint(reads_blueprint, url_prefix="/interaction_api")

    from project.api.likes import likes_blueprint
    app.register_blueprint(likes_blueprint, url_prefix="/interaction_api")

    return
