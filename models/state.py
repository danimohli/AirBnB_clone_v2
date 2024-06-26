#!/usr/bin/python3
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class State(BaseModel, Base):
    """
    State class that inherits from BaseModel and Base.
    """
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="all, delete, delete-orphan")

    @property
    def cities(self):
        """
        Getter attribute in case of FileStorage
        """
        return [city for city in models.storage.all(City).values() if city.state_id == self.id]
