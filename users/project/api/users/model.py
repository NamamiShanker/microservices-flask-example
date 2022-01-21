"""User model"""
import datetime
from enum import unique

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID

from project.extensions import db
from project.lib import ResourceMixin

class User(ResourceMixin, db.Model):
	
	__tablename__ = 'users'

	user_id = db.Column(
		UUID(as_uuid=True),
		unique=True,
		server_default=text("uuid_generate_v4()"),
		nullable=False,
		primary_key=True,
		index=True
	)

	first_name = db.Column(db.String(120), nullable=False)
	last_name = db.Column(db.String(120), nullable=False)
	email_id = db.Column(db.String(120), nullable=False, unique=True)
	phone_number = db.Column(db.String(120), nullable=False, unique=True)