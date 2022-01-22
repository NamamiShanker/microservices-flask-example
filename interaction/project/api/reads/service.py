import os
import requests
from uuid import UUID

from project.lib import BadRequest, validate_user

from .interface import ReadInterface

def get_read_by_id(read_id: UUID):
	return ReadInterface.get_read_by_id(read_id)

def get_reads_by_content_id(content_id: UUID):
	return ReadInterface.get_reads_by_content_id(content_id)

def create_new_read(read_data: dict):
	validate_user(read_data.get("user_id"))
	return ReadInterface.create_read(read_data)

def get_all_reads(skip, limit):
	return ReadInterface.get_all_reads(skip, limit)