import os
from uuid import UUID

from flask import Blueprint, request
from flask.views import MethodView
from marshmallow import ValidationError
from werkzeug.utils import secure_filename

from .service import (
    get_all_contents,
    create_new_content,
    get_content_by_id,
    delete_content_by_id,
    update_content_by_id,
    allowed_file,
    get_sorted_content_by_date,
    get_sorted_content_by_reads_or_likes
)
from .schema import (
    all_contents_schema,
    create_content_schema,
    content_out_schema,
    update_content_schema,
    sorted_content_schema
)

from project.lib import BadRequest, ServerError
from project.tasks import ingest_csv_task

contents_blueprint = Blueprint("contents", __name__)


class ContentsList(MethodView):
    """Multiple contents Post and Get methods"""

    @staticmethod
    def get(skip: int = 0, limit: int = 100):
        """Get all contents"""
        try:
            contents = get_all_contents(skip, limit)
            resp = all_contents_schema.dump(contents)
        except BadRequest as err:
            raise BadRequest(message=err.message, status=err.status)
        except Exception as e:
            raise ServerError(message=str(e), status=500)
        else:
            return {"contents_list": resp}, 200

    @staticmethod
    def post():
        """Create a new content"""
        val = create_content_schema.validate(request.json)
        if val:
            raise BadRequest(val, status=400)
        try:
            data = request.get_json()
            u = create_content_schema.load(data)
            created_content = create_new_content(u)
            resp = content_out_schema.dump(created_content)
        except ValidationError as err:
            raise BadRequest(message=str(err), status=422)
        except BadRequest as err:
            raise BadRequest(message=err.message, status=err.status)
        except Exception as e:
            raise ServerError(message=str(e), status=500)
        else:
            return {"content": resp}, 201


class ContentsView(MethodView):
    """Individual content specific methods"""

    @staticmethod
    def get(content_id: UUID):
        """Get a content by id"""
        try:
            content = get_content_by_id(content_id)
            resp = content_out_schema.dump(content)
        except BadRequest as err:
            raise BadRequest(message=err.message, status=err.status)
        except Exception as e:
            raise ServerError(message=str(e), status=500)
        else:
            return {"content": resp}, 200

    @staticmethod
    def delete(content_id: UUID):
        """Delete a content by id"""
        try:
            delete_content_by_id(content_id)
        except BadRequest as err:
            raise BadRequest(message=err.message, status=err.status)
        except Exception as e:
            raise ServerError(message=str(e), status=500)
        else:
            return {"message": "content deleted"}, 204

    @staticmethod
    def put(content_id: UUID):
        """Update a content by id"""
        val = update_content_schema.validate(request.json)
        if val:
            raise BadRequest(val, status=400)
        try:
            data = request.get_json()
            u = update_content_schema.load(data)
            updated_content = update_content_by_id(content_id, u)
            resp = content_out_schema.dump(updated_content)
        except ValidationError as err:
            raise BadRequest(message=err.messages, status=422)
        except BadRequest as err:
            raise BadRequest(message=err.message, status=err.status)
        except Exception as e:
            raise ServerError(message=str(e), status=500)
        else:
            return {"content": resp}, 200


def ingest_csv():
    """Ingest data from a csv file"""
    if "file" not in request.files:
        raise BadRequest("No file part", status=400)
    file = request.files["file"]
    if file.filename == "":
        raise BadRequest("No selected file", status=400)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(os.environ.get("UPLOAD_FOLDER", "./uploads"), filename)
        file.save(file_path)
        ingest_csv_task.apply_async(args=[file_path])
        return "File uploaded successfully", 200

def get_sorted_contents():
    try:
        data = request.get_json()
        u = sorted_content_schema.load(data)
        if u["sort_by"] == 'date':
            content = get_sorted_content_by_date(u["order"])
        else:
            content = get_sorted_content_by_reads_or_likes(u["sort_by"], u["order"])
        resp = all_contents_schema.dump(content)
    except ValidationError as err:
        raise BadRequest(message=err.messages, status=422)
    except BadRequest as err:
        raise BadRequest(message=err.message, status=err.status)
    except Exception as e:
        raise ServerError(message=str(e), status=500)
    return {"content": resp}, 200

contents_blueprint.add_url_rule(
    "/contents",
    view_func=ContentsList.as_view("contents_list"),
    methods=["GET", "POST"],
)

contents_blueprint.add_url_rule(
    "/contents/<uuid:content_id>",
    view_func=ContentsView.as_view("contents_view"),
    methods=["GET", "DELETE", "PUT"],
)

contents_blueprint.add_url_rule(
    "/ingest", view_func=ingest_csv, methods=["POST"]
)

contents_blueprint.add_url_rule(
    "/sorted", view_func=get_sorted_contents, methods=["POST"]
)