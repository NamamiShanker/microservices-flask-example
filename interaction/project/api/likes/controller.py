import os
from uuid import UUID

from flask import Blueprint, request
from flask.views import MethodView
from marshmallow import ValidationError

from .service import create_new_like, get_all_likes, get_like_by_id, get_likes_by_content_id
from .schema import all_likes_schema, create_like_schema, like_out_schema

from project.lib import BadRequest, ServerError

likes_blueprint = Blueprint("likes", __name__)

class LikesList(MethodView):
	"""Multiple likes Post and Get methods"""

	@staticmethod
	def get(skip: int = 0, limit: int = 100):
		"""Get all likes"""
		try:
			likes = get_all_likes(skip, limit)
			resp = all_likes_schema.dump(likes)
		except BadRequest as err:
			raise BadRequest(message=err.message, status=err.status)
		except Exception as e:
			raise ServerError(message=str(e), status=500)
		else:
			return {"likes_list": resp}, 200

	@staticmethod
	def post():
		"""Create a new like"""
		val = create_like_schema.validate(request.json)
		if val:
			raise BadRequest(val, status=400)
		try:
			data = request.get_json()
			u = create_like_schema.load(data)
			created_like = create_new_like(u)
			resp = like_out_schema.dump(created_like)
		except ValidationError as err:
			raise BadRequest(message=str(err), status=422)
		except BadRequest as err:
			raise BadRequest(message=err.message, status=err.status)
		else:
			return {"like": resp}, 201

class LikesView(MethodView):
	"""Single like Get and Delete methods"""

	@staticmethod
	def get(like_id: UUID):
		"""Get a like by id"""
		try:
			like = get_like_by_id(like_id)
			resp = like_out_schema.dump(like)
		except BadRequest as err:
			raise BadRequest(message=err.message, status=err.status)
		except Exception as e:
			raise ServerError(message=str(e), status=500)
		else:
			return {"like": resp}, 200

likes_blueprint.add_url_rule(
	"/likes",
	view_func=LikesList.as_view("likes_list"),
	methods=["GET", "POST"],
)

likes_blueprint.add_url_rule(
	"/likes/<uuid:like_id>",
	view_func=LikesView.as_view("like"),
	methods=["GET"],
)