from uuid import UUID
from .interface import UserInterface

def get_user_by_id(id: UUID):
	"""Get a user by id"""
	return UserInterface.get_user_by_id(id)

def get_all_users(skip: int = 0, limit: int = 100):
	"""Get all users"""
	return UserInterface.get_all_users(skip, limit)

def create_new_user(user_in):
	"""Create a new user"""
	return UserInterface.create_user(user_in)

def delete_user_by_id(id: UUID):
	"""Delete a user by id"""
	return UserInterface.delete_user_by_id(id)

def update_user_by_id(id: UUID, user_in):
	"""Update a user by id"""
	return UserInterface.update_user_by_id(id, user_in)