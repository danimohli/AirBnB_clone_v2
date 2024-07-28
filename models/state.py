#!/usr/bin/python3
"""
State class for managing State objects.
"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import Base, BaseModel
from models.city import City


class State(BaseModel, Base):
    """
    Represents a state.
    """

    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="all, delete, delete-orphan")

    def cities(self):
        """
        Returns a list of City objects linked to the current State.
        """
        if isinstance(storage, DBStorage):
            return [city for city in storage.all(City).values() if city.state_id == self.id]
        else:
            return [city for city in storage.all(City).values() if city.state_id == self.id]
