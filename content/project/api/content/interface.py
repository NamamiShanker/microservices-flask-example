from uuid import UUID
from dataclasses import dataclass
from sqlalchemy import desc, asc

from .model import Content as ContentDB
from project.lib import ServerError


@dataclass
class ContentInterface:

    content_id: UUID
    title: str
    story: str
    date: str
    user_id: UUID

    @classmethod
    def interface_creator(cls, content_db: ContentDB):
        return cls(
            content_id=content_db.content_id,
            title=content_db.title,
            story=content_db.story,
            date=content_db.date,
            user_id=content_db.user_id,
        )

    @classmethod
    def get_all_contents(cls, skip, limit):
        """Get all content"""
        contents_db = ContentDB.query.limit(limit).offset(skip).all()
        return [cls.interface_creator(content_db) for content_db in contents_db]

    @classmethod
    def get_content_by_id(cls, content_id: UUID):
        content_db = ContentDB.get_first({"content_id": content_id})
        if content_db:
            return cls.interface_creator(content_db=content_db)
        return None

    @classmethod
    def update_content_by_id(cls, content_id: UUID, content_data: dict):
        content_db = ContentDB.get_first({"content_id": content_id})
        if content_db:
            content_db = content_db.update(**content_data)
            return cls.interface_creator(content_db=content_db)
        return None

    @classmethod
    def delete_content_by_id(cls, content_id: UUID):
        content_db = ContentDB.get_first({"content_id": content_id})
        if content_db:
            content_db.delete()
            return True
        return False

    @classmethod
    def create_content(cls, content_data: dict):
        content_db = ContentDB(
            title=content_data.get("title"),
            story=content_data.get("story"),
            date=content_data.get("date"),
            user_id=content_data.get("user_id"),
        )
        content_db.create()
        if content_db:
            return cls.interface_creator(content_db)
        return None

    @classmethod
    def create_bulk_content(cls, content_data: list):
        try:
            ContentDB.create_bulk(content_data)
        except Exception as e:
            raise ServerError(message=str(e), status=400)
        return None

    @classmethod
    def get_sorted_content_by_date(cls, order_by):
        if(order_by == "desc"):
            contents_db = ContentDB.query.order_by(desc(ContentDB.date)).all()
        else:
            contents_db = ContentDB.query.order_by(asc(ContentDB.date)).all()
        return [cls.interface_creator(content_db) for content_db in contents_db]