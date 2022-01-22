import os
import requests
from uuid import UUID

from project.lib import BadRequest, validate_user

from .interface import LikeInterface

def get_like_by_id(like_id: UUID):
	return LikeInterface.get_like_by_id(like_id)

def get_likes_by_content_id(content_id: UUID):
	return LikeInterface.get_likes_by_content_id(content_id)

def create_new_like(like_data: dict):
	validate_user(like_data.get("user_id"))
	return LikeInterface.create_like(like_data)

def get_all_likes(skip, limit):
	return LikeInterface.get_all_likes(skip, limit)