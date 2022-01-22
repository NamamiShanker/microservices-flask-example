"""
Here you will find the core models and abstract functions
which will be acting as a abstract base extract class, following the
Model Inheritance
"""
from typing import Any, Dict, Optional, List

from sqlalchemy import func, true

from project.extensions import db


class ResourceMixin(db.Model):
    """A base abstract class model
    :param DateTime 'created_on': Datetime on which a particular model was created default to server
    :param DateTime 'updated_on': Datetime on which a particular model was updated default to server
    :param Boolean 'active': Whether the instance is active, if not it should be considered as Marked for deletion
    """

    __abstract__ = True

    created_on = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_on = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
    )
    active = db.Column(db.Boolean(), server_default=true(), nullable=False)

    def __str__(self):
        """
        Creates a human readable version of the class instance
        :return: self string
        """
        obj_id = hex(id(self))
        columns = self.__table__.c.keys()

        values = ", ".join(f"{n}={getattr(self, n)}" for n in columns)
        return f"<{obj_id} {self.__class__} {values}>"

    def create(self):
        """Save a model Instance to the database
        :return: self
        :except: return error
        """
        try:
            db.session.add(self)
            db.session.commit()
            db.session.refresh(self)
        except Exception as e:
            db.session.rollback()
            raise e
        else:
            return self

    def update(self, **kwargs):
        """
        Update the model Instance
        :param kwargs: Attributes
        :return: db.session.commit()'s result
        """
        try:
            for attr, value in iter(kwargs.items()):
                setattr(self, attr, value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        else:
            return self

    def delete(self, force_delete=True):
        """
        Delete a model instance.
        :return: db.session.commit()'s result
        :except: returns error
        """
        try:
            if force_delete is True:
                db.session.delete(self)
            else:
                setattr(self, "active", False)
        except Exception as e:
            db.session.rollback()
            raise e
        else:
            db.session.commit()
            return True

    @classmethod
    def get_first(cls, kwargs: Dict[str, Any]):
        """
        Gets the query single result object as per query passed
        :param kwargs: Key and value associated to respective column
        :return:
        """
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def get_all(cls, kwargs: Optional[Dict[str, Any]] = None):
        """
        Gets the query list result as per query passed
        :param kwargs: Key and value associated to respective column
        :return:
        """
        if kwargs is not None:
            return cls.query.filter_by(**kwargs).all()
        return cls.query.all()

    @classmethod
    def create_bulk(cls, bulk_data: List[Dict[str, Any]]):
        try:
            db.session.bulk_insert_mappings(cls, bulk_data)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        else:
            return

    @classmethod
    def update_bulk(cls, bulk_data: List[Dict[str, Any]]):
        try:
            db.session.bulk_update_mappings(cls, bulk_data)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        else:
            return

