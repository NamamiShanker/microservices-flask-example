from marshmallow import Schema, fields

class BaseUser(Schema):
	first_name = fields.Str()
	last_name = fields.Str()
	email_id = fields.Email()
	phone_number = fields.Str()

class UserOut(BaseUser):
	user_id = fields.UUID(required=True)

class UserCreate(BaseUser):
	pass

all_users_schema = UserOut(many=True)
create_user_schema = UserCreate()
user_out_schema = UserOut()