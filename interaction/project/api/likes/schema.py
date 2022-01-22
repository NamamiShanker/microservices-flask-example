from marshmallow import Schema, fields

class BaseLike(Schema):
	user_id = fields.UUID(required=True)
	content_id = fields.UUID(required=True)

class LikeOut(BaseLike):
	like_id = fields.UUID(required=True)

class LikeCreate(BaseLike):
	pass

all_likes_schema = LikeOut(many=True)
create_like_schema = LikeCreate()
like_out_schema = LikeOut()
