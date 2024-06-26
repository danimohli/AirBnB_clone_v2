#!/usr/bin/python3
"""
Custom base class for the entire project
"""

from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import models

Base = declarative_base()


class BaseModel:
    """
    Basemodel for all the classes
    """

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """Public instance artributes initialization
        """

        dtf = '%Y-%m-%dT%H:%M:%S.%f'
        if not kwargs:
            self.id = str(uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
        else:
            for k, v in kwargs.items():
                if k in ("updated_at", "created_at"):
                    self.__dict__[k] = datetime.strptime(v, dtf)
                elif k == "id":
                    self.__dict__[k] = str(v)
                else:
                    self.__dict__[k] = v
            if "id" not in kwargs:
                self.id = str(uuid4())
            if "created_at" not in kwargs:
                self.created_at = datetime.utcnow()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.utcnow()

    def __str__(self):
        """
        Returns string representation
        """
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """
        Updates the public instance attribute: updated_at
        with the current datetime
        """
        self.updated_at = datetime.utcnow()
        models.storage.new(self)  # moved here from __init__
        models.storage.save()

    def to_dict(self):
        """
        Method returns a dictionary containing all
        keys/values of __dict__ instance
        """
        obj_m = {}
        for k, v in self.__dict__.items():
            if k == "created_at" or k == "updated_at":
                obj_m[k] = v.isoformat()
            elif k != "_sa_instance_state":
                obj_m[k] = v
        obj_m["__class__"] = self.__class__.__name__
        return obj_m

    def delete(self):
        """
        Delete the current instance from the storage
        """
        models.storage.delete(self)
