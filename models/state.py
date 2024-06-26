#!/usr/bin/python3
"""
Contains the State class
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City
import models


class State(BaseModel, Base):
    """
    State class
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="all, delete,
                          delete-orphan", backref="state")

    @property
    def cities(self):
        """
        Getter attribute cities that returns the list of City instances
        """
        if models.storage_t == 'db':
            return self.cities
        else:
            return [city for city in models.storage.all(City).values()
                    if city.state_id == self.id]
