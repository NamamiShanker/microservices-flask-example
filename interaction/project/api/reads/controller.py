import os
from uuid import UUID

from flask import Blueprint, request
from flask.views import MethodView
from marshmallow import ValidationError

from .service import create_new_read, get_all_reads, get_read_by_id, get_reads_by_content_id
from .schema import all_reads_schema, create_read_schema, read_out_schema

from project.lib import BadRequest, ServerError

reads_blueprint = Blueprint("reads", __name__)

class ReadsList(MethodView):
	"""Multiple reads Post and Get methods"""

	@staticmethod
	def get(skip: int = 0, limit: int = 100):
		"""Get all reads"""
		try:
			reads = get_all_reads(skip, limit)
			resp = all_reads_schema.dump(reads)
		except BadRequest as err:
			raise BadRequest(message=err.message, status=err.status)
		except Exception as e:
			raise ServerError(message=str(e), status=500)
		else:
			return {"reads_list": resp}, 200

	@staticmethod
	def post():
		"""Create a new read"""
		val = create_read_schema.validate(request.json)
		if val:
			raise BadRequest(val, status=400)
		try:
			data = request.get_json()
			u = create_read_schema.load(data)
			created_read = create_new_read(u)
			resp = read_out_schema.dump(created_read)
		except ValidationError as err:
			raise BadRequest(message=str(err), status=422)
		except BadRequest as err:
			raise BadRequest(message=err.message, status=err.status)
		else:
			return {"read": resp}, 201

class ReadsView(MethodView):
	"""Single read Get and Delete methods"""

	@staticmethod
	def get(read_id: UUID):
		"""Get a read by id"""
		try:
			read = get_read_by_id(read_id)
			resp = read_out_schema.dump(read)
		except BadRequest as err:
			raise BadRequest(message=err.message, status=err.status)
		except Exception as e:
			raise ServerError(message=str(e), status=500)
		else:
			return {"read": resp}, 200

reads_blueprint.add_url_rule(
	"/reads",
	view_func=ReadsList.as_view("reads_list"),
	methods=["GET", "POST"],
)

reads_blueprint.add_url_rule(
	"/reads/<uuid:read_id>",
	view_func=ReadsView.as_view("read"),
	methods=["GET", "DELETE"],
)