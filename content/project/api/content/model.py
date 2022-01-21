"""User model"""
import datetime

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID

from project.extensions import db
from project.lib import ResourceMixin


class Content(ResourceMixin, db.Model):

    __tablename__ = "content"

    content_id = db.Column(
        UUID(as_uuid=True),
        unique=True,
        server_default=text("uuid_generate_v4()"),
        nullable=False,
        primary_key=True,
        index=True,
    )

    title = db.Column(db.String(120), nullable=False)
    story = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    user_id = db.Column(UUID(as_uuid=True), nullable=False)
