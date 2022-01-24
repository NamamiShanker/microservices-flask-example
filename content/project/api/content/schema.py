from marshmallow import Schema, fields, validate


class BaseContent(Schema):
    title = fields.Str()
    story = fields.Str()


class ContentOut(BaseContent):
    content_id = fields.UUID(required=True)
    date = fields.DateTime("%d-%m-%Y %H:%M:%S")
    user_id = fields.UUID(required=True)


class ContentCreate(BaseContent):
    date = fields.DateTime("%d-%m-%Y %H:%M:%S")
    user_id = fields.UUID(required=True)
    pass


class ContentUpdate(BaseContent):
    pass


all_contents_schema = ContentOut(many=True)
create_content_schema = ContentCreate()
update_content_schema = ContentUpdate()
content_out_schema = ContentOut()
create_bulk_content_schema = ContentCreate(many=True)