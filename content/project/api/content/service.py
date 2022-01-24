from uuid import UUID

from .interface import ContentInterface
from .schema import create_bulk_content_schema

from project.lib.api_utils import get_read_list_by_content_id_list, get_like_list_by_content_id_list

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

def get_sorted_content_by_date(order_by: str = "desc"):
    return ContentInterface.get_sorted_content_by_date(order_by)

def get_sorted_content_by_reads_or_likes(sort_by: str = "reads", order_by: str = "desc"):
    contents = get_all_contents()
    content_ids = [str(content.content_id) for content in contents]
    reads = get_read_list_by_content_id_list(content_ids)['content_list'] if sort_by == "reads" else get_like_list_by_content_id_list(content_ids)['content_list']
    for content in reads:
        reads[content] = len(reads[content])
    sorted_reads = dict(sorted(reads.items(), key=lambda item: item[1]))
    return [
        ContentInterface.get_content_by_id(content_id)
        for content_id in sorted_reads
    ][::-1] if order_by == "desc" else [
        ContentInterface.get_content_by_id(content_id)
        for content_id in sorted_reads
    ]