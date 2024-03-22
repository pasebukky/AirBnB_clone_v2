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
        """ Getter attribute to return related cities """
        if models.storage.__class__.__name__ != 'DBStorage':
            return [city for city in models.storage.all(City)
                    if city.state_id == self.id]
        else:
            return self.cities
