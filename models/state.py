#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String
import models
from models.city import City
import shlex
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship(
            "City",
            cascade='all, delete, delete-orphan',
            backref="state")

    @property
    def cities(self):
        variable = models.storage.all()
        rlist = []
        res = []
        for k in variable:
            city = k.replace(".", " ")
            city = shlex.split(city)
            if (city[0] == "City"):
                rlist.append(variable[k])
        for element in rlist:
            if (element.state_id == self.id):
                res.append(element)
        return (res)
