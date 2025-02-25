#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from os import getenv
import models
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id", String(60),
                             ForeignKey("places.id"),
                             primary_key=True,
                             nullable=False),
                      Column("amenity_id", String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=False)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship(
                  "Review", cascade='all, delete, delete-orphan',
                  backref="place")

        amenities = relationship(
                    "Amenity",
                    secondary=place_amenity, viewonly=False,
                    back_populates="place_amenities")

    @property
    def reviews(self):
        """
        Getter aattribute for reviews
        """
        variable = models.storage.all()
        rlist = []
        res = []
        for k in variable:
            review = k.replace(".", " ")
            review = shlex.split(review)
            if (review[0] == "Review"):
                rlist.append(variable[k])
        for element in rlist:
            if (element.place_id == self.id):
                res.append(element)
        return (res)

    @property
    def amenities(self):
        """
        list of amenity ids
        """
        return self.amenity_ids

    @amenities.setter
    def amenities(self, obj=None):
        """
        Amenity ids appended to the attribute
        """
        if type(obj) is Amenity and obj.id not in self.amenity_ids:
            self.amenity_ids.append(obj.id)
