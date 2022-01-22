import os
import requests

def get_read_list_by_content_id_list(content_id_list: list):
	r = requests.post(
		url=os.environ.get("INTERACTION_API_URL") + "/interaction_api/reads/content/bulk",
		json={"ids": content_id_list},
	)
	return r.json()

def get_like_list_by_content_id_list(content_id_list: list):
	r = requests.post(
		url=os.environ.get("INTERACTION_API_URL") + "/interaction_api/likes/content/bulk",
		json={"ids": content_id_list},
	)
	return r.json()