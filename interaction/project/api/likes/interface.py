from uuid import UUID
from dataclasses import dataclass

from .model import Like as LikeDB
from project.lib import BadRequest

@dataclass
class LikeInterface:

	like_id: UUID
	user_id: UUID
	content_id: UUID

	@classmethod
	def interface_creator(cls, like_db: LikeDB):
		return cls(
			like_id=like_db.like_id,
			user_id=like_db.user_id,
			content_id=like_db.content_id,
		)

	@classmethod
	def get_all_likes(cls, skip, limit):
		"""Get all likes"""
		likes_db = LikeDB.query.limit(limit).offset(skip).all()
		return [cls.interface_creator(like_db) for like_db in likes_db]
	
	@classmethod
	def get_like_by_id(cls, like_id: UUID):
		like_db = LikeDB.get_first({"like_id": like_id})
		if like_db:
			return cls.interface_creator(like_db=like_db)
		return None
	
	@classmethod
	def get_likes_by_content_id(cls, content_id: UUID):
		likes_db = LikeDB.get_all({"content_id": content_id})
		if likes_db:
			return [cls.interface_creator(like_db) for like_db in likes_db]
		return []

	@classmethod
	def create_like(cls, like_data: dict):
		like_db = LikeDB.get_first({"user_id": like_data["user_id"], "content_id": like_data["content_id"]})
		if like_db:
			raise BadRequest("Like already exists", 409)
		like_db = LikeDB(
			user_id=like_data.get("user_id"),
			content_id=like_data.get("content_id"),
		)
		like_db.create()
		return cls.interface_creator(like_db=like_db)
	