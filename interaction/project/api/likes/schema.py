from marshmallow import Schema, fields

class BaseLike(Schema):
	user_id = fields.UUID(required=True)
	content_id = fields.UUID(required=True)

class LikeOut(BaseLike):
	like_id = fields.UUID(required=True)

class LikeCreate(BaseLike):
	pass

class IDList(Schema):
	ids = fields.List(fields.UUID(required=True))

all_likes_schema = LikeOut(many=True)
create_like_schema = LikeCreate()
like_out_schema = LikeOut()
id_list_schema = IDList()