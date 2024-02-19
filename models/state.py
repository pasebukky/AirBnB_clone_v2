#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
import models


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade='all, delete, delete-orphan',
                          backref="state")

    @property
    def related_cities(self):
        """ File storage getter attribute """
        all_objects = storage.all()
        city_instances = []

        for key, obj in all_objects.items():
            if isinstance(obj, models.City) and obj.state_id == self.id:
                city_instances.append(obj)

        return city_instances
