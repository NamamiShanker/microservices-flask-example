from typing import List
from uuid import UUID

from project.lib import BadRequest, validate_user

from .interface import LikeInterface

def get_like_by_id(like_id: UUID):
	return LikeInterface.get_like_by_id(like_id)

def get_user_likes_by_content_id(content_id: UUID):
	likes = LikeInterface.get_likes_by_content_id(content_id)
	return [like.user_id for like in likes]

def get_user_likes_by_content_id_bulk(content_ids: List[UUID]):
	print("Getting content ids:", content_ids)
	return {
	    str(content_id): get_user_likes_by_content_id(content_id)
	    for content_id in content_ids
	}

def get_likes_by_content_id(content_id: UUID):
	return LikeInterface.get_likes_by_content_id(content_id)

def create_new_like(like_data: dict):
	validate_user(like_data.get("user_id"))
	return LikeInterface.create_like(like_data)

def get_all_likes(skip, limit):
	return LikeInterface.get_all_likes(skip, limit)