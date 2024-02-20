#!/usr/bin/python3
""" Place Module for HBNB project """
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from os import getenv
import models


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    reviews = relationship("Review", cascade='all, delete, delete-orphan', backref="place")

    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE", None) != "db":
        @property
        def reviews(self):
            """return the list of reviews for a place using FileStorage"""
            all_reviews = []
            for review in list(models.storage.all(Review).values()):
                if review.place_id == self.id:
                    all_reviews.append(review)
            return all_reviews

