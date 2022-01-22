from marshmallow import Schema, fields

class BaseRead(Schema):
	user_id = fields.UUID(required=True)
	content_id = fields.UUID(required=True)

class ReadOut(BaseRead):
	read_id = fields.UUID(required=True)

class ReadCreate(BaseRead):
	pass

all_reads_schema = ReadOut(many=True)
create_read_schema = ReadCreate()
read_out_schema = ReadOut()
