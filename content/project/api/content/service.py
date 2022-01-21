from uuid import UUID

from .interface import ContentInterface
from .schema import create_bulk_content_schema

ALLOWED_EXTENSIONS = {"csv"}


def get_content_by_id(id: UUID):
    """Get a content by id"""
    return ContentInterface.get_content_by_id(id)


def get_all_contents(skip: int = 0, limit: int = 100):
    """Get all contents"""
    return ContentInterface.get_all_contents(skip, limit)


def create_new_content(content_in):
    """Create a new content"""
    return ContentInterface.create_content(content_in)


def delete_content_by_id(id: UUID):
    """Delete a content by id"""
    return ContentInterface.delete_content_by_id(id)


def update_content_by_id(id: UUID, content_in):
    """Update a content by id"""
    return ContentInterface.update_content_by_id(id, content_in)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def ingest_json_content(data: list):
    data = create_bulk_content_schema.load(data)
    ContentInterface.create_bulk_content(data)