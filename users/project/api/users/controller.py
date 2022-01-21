from uuid import UUID

from flask import Blueprint, request
from flask.views import MethodView
from marshmallow import ValidationError

from .service import get_all_users, create_new_user, get_user_by_id, delete_user_by_id, update_user_by_id
from .schema import all_users_schema, create_user_schema, user_out_schema

from project.lib import BadRequest, ServerError

users_blueprint = Blueprint('users', __name__)

class UsersList(MethodView):
	"""Multiple users Post and Get methods"""
	@staticmethod
	def get(skip: int = 0, limit: int = 100):
		"""Get all users"""
		try:
			users = get_all_users(skip, limit)
			resp = all_users_schema.dump(users)
		except BadRequest as err:
			raise BadRequest(message=err.message, status=err.status)
		except Exception as e:
			raise ServerError(message=str(e), status=500)
		else:
			return {'users_list': resp}, 200

	@staticmethod
	def post():
		"""Create a new user"""
		val = create_user_schema.validate(request.json)
		if val:
			raise BadRequest(val, status=400)
		try:
			data = request.get_json()
			u = create_user_schema.load(data)
			created_user = create_new_user(u)
			resp = user_out_schema.dump(created_user)
		except ValidationError as err:
			raise BadRequest(message=str(err), status=422)
		except BadRequest as err:
			raise BadRequest(message=err.message, status=err.status)
		except Exception as e:
			raise ServerError(message=str(e), status=500)
		else:
			return {'user': resp}, 201

class UsersView(MethodView):
	"""Individual User specific methods"""

	@staticmethod
	def get(user_id: UUID):
		"""Get a user by id"""
		try:
			user = get_user_by_id(user_id)
			resp = user_out_schema.dump(user)
		except BadRequest as err:
			raise BadRequest(message=err.message, status=err.status)
		except Exception as e:
			raise ServerError(message=str(e), status=500)
		else:
			return {'user': resp}, 200

	@staticmethod
	def delete(user_id: UUID):
		"""Delete a user by id"""
		try:
			delete_user_by_id(user_id)
		except BadRequest as err:
			raise BadRequest(message=err.message, status=err.status)
		except Exception as e:
			raise ServerError(message=str(e), status=500)
		else:
			return {'message': 'User deleted'}, 204

	@staticmethod
	def put(user_id: UUID):
		"""Update a user by id"""
		val = create_user_schema.validate(request.json)
		if val:
			raise BadRequest(val, status=400)
		try:
			data = request.get_json()
			u = create_user_schema.load(data)
			updated_user = update_user_by_id(user_id, u)
			resp = user_out_schema.dump(updated_user)
		except ValidationError as err:
			raise BadRequest(message=str(err), status=422)
		except BadRequest as err:
			raise BadRequest(message=err.message, status=err.status)
		except Exception as e:
			raise ServerError(message=str(e), status=500)
		else:
			return {'user': resp}, 200

users_blueprint.add_url_rule(
	"/users",
	view_func=UsersList.as_view("users_list"),
	methods=["GET", "POST"]
)

users_blueprint.add_url_rule(
	"/users/<uuid:user_id>",
	view_func=UsersView.as_view("users_view"),
	methods=["GET", "DELETE", "PUT"]
)