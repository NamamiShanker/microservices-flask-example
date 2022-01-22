import os
import requests
from uuid import UUID
from .errors import BadRequest

def validate_user(user_id: UUID):
	r = requests.get(os.environ.get("USER_API_URL") + f"/user_api/users/{user_id}")
	if(r.status_code == 200):
		return True
	else:
		raise BadRequest("User not found", status=400)