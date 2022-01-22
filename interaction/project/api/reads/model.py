from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID

from project.extensions import db
from project.lib import ResourceMixin


class Read(ResourceMixin, db.Model):

	__tablename__ = "reads"

	read_id = db.Column(
		UUID(as_uuid=True),
		unique=True,
		server_default=text("uuid_generate_v4()"),
		nullable=False,
		primary_key=True,
		index=True,
	)

	user_id = db.Column(UUID(as_uuid=True), nullable=False)
	content_id = db.Column(UUID(as_uuid=True), nullable=False)
