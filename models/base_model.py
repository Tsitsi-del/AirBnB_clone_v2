#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import models


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), primary_key=True, unique=True,
                nullable=False)
    created_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow())
    update_at = Column(DateTime, nullable=False,
                       default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if kwargs:
            for k, val in kwargs.items():
                if k == "created_at" or k == "updated_at":
                    val = datetime.strptime(val, "%Y-%m-%dT%H:%M:%S.%f")
                if k != "__class__":
                    setattr(self, k, val)
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            if "updated_at" not in kwargs:
                self.updated_at = datetime.now()
            if "created_at" not in kwargs:
                self.created_at = datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()

    def __str__(self):
        """Returns a string representation of the instance"""
        return f"[{type(self).__name__} ({self.id}) {self.__dict__}]"

    def __repr__(self):
        """
        string representation
        """
        return self.__str__()

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        Creates a dictionary with object attributes
        adds a key for the class name used to create
        object from dictionary by checking class key
        """
        dict_obj = dict(self.__dict__)
        dict_obj['__class__'] = str(type(self).__name__)
        dict_obj['created_at'] = self.created_at.isoformat()
        dict_obj['updated_at'] = self.updated_at.isoformat()
        if "_sa_instance_state" in dict_obj.keys():
            del dict_obj["_sa_instance_state"]
        return (dict_obj)

    def delete(self):
        """
        delete an instance
        """
        models.storage.delete(self)
