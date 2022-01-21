from uuid import UUID
from dataclasses import dataclass

from .model import User as UserDB

@dataclass
class UserInterface:

	user_id: UUID
	first_name: str
	last_name: str
	email_id: str
	phone_number: str

	@classmethod
	def interface_creator(cls, user_db: UserDB):
		return cls(
			user_id=user_db.user_id,
			first_name=user_db.first_name,
			last_name=user_db.last_name,
			email_id=user_db.email_id,
			phone_number=user_db.phone_number
		)
	
	@classmethod
	def get_all_users(cls, skip, limit):
		"""Get all users"""
		users_db = UserDB.query.limit(limit).offset(skip).all()
		return [cls.interface_creator(user_db) for user_db in users_db]
	
	@classmethod
	def get_user_by_id(cls, user_id: UUID):
		user_db = UserDB.get_first({"user_id": user_id})
		if user_db:
			return cls.interface_creator(user_db)
		return None
	
	@classmethod
	def update_user_by_id(cls, user_id: UUID, user_data: dict):
		user_db = UserDB.get_first({"user_id": user_id})
		if user_db:
			user_db = user_db.update(**user_data)
			return cls.interface_creator(user_db)
		return None

	@classmethod
	def delete_user_by_id(cls, user_id: UUID):
		user_db: UserDB = UserDB.get_first({"user_id": user_id})
		if user_db:
			user_db.delete()
			return True
		return False

	@classmethod
	def create_user(cls, user_data: dict):
		user_db = UserDB(
			first_name=user_data.get("first_name"),
			last_name=user_data.get("last_name"),
			email_id=user_data.get("email_id"),
			phone_number=user_data.get("phone_number")
		)
		user_db.create()
		if user_db:
			return cls.interface_creator(user_db)
		return None