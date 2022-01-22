from uuid import UUID
from dataclasses import dataclass

from .model import Read as ReadDB
from project.lib import BadRequest

@dataclass
class ReadInterface:

	read_id: UUID
	user_id: UUID
	content_id: UUID

	@classmethod
	def interface_creator(cls, read_db: ReadDB):
		return cls(
			read_id=read_db.read_id,
			user_id=read_db.user_id,
			content_id=read_db.content_id,
		)

	@classmethod
	def get_all_reads(cls, skip, limit):
		"""Get all reads"""
		reads_db = ReadDB.query.limit(limit).offset(skip).all()
		return [cls.interface_creator(read_db) for read_db in reads_db]
	
	@classmethod
	def get_read_by_id(cls, read_id: UUID):
		read_db = ReadDB.get_first({"read_id": read_id})
		if read_db:
			return cls.interface_creator(read_db=read_db)
		return None
	
	@classmethod
	def get_reads_by_content_id(cls, content_id: UUID):
		reads_db = ReadDB.get_all({"content_id": content_id})
		if reads_db:
			return [cls.interface_creator(read_db) for read_db in reads_db]
		return None

	@classmethod
	def create_read(cls, read_data: dict):
		read_db = ReadDB.get_first({"user_id": read_data["user_id"], "content_id": read_data["content_id"]})
		if read_db:
			raise BadRequest("Read already exists", 409)
		read_db = ReadDB(
			user_id=read_data.get("user_id"),
			content_id=read_data.get("content_id"),
		)
		read_db.create()
		return cls.interface_creator(read_db=read_db)
	