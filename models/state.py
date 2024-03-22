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

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        cities = relationship("City", cascade='all, delete, delete-orphan',
                              backref="state")

    else:

        @property
        def cities(self):
            """ Returns the list of City instances with
            state_id == current State.id """
            all_cities = models.storage.all(City)
            state_cities = []
            for city_ins in all_cities.values():
                if city_ins.state_id == self.id:
                    state_cities.append(city_ins)

            return state_cities
