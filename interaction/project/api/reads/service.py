from typing import List
from uuid import UUID

from project.lib import BadRequest, validate_user

from .interface import ReadInterface

def get_read_by_id(read_id: UUID):
	return ReadInterface.get_read_by_id(read_id)

def get_user_reads_by_content_id(content_id: UUID):
	reads = ReadInterface.get_reads_by_content_id(content_id)
	return [read.user_id for read in reads]

def get_user_reads_by_content_id_bulk(content_ids: List[UUID]):
	return {
	    str(content_id): get_user_reads_by_content_id(content_id)
	    for content_id in content_ids
	}

def create_new_read(read_data: dict):
	validate_user(read_data.get("user_id"))
	return ReadInterface.create_read(read_data)

def get_all_reads(skip, limit):
	return ReadInterface.get_all_reads(skip, limit)