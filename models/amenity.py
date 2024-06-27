#!/usr/bin/python3
"""
Amenity module
"""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.place import place_amenity

class Amenity(BaseModel, Base):
    """
    Amenity class that inherits from BaseModel and Base.
    """
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
    place_amenities = relationship('Place', secondary=place_amenity,
                                   back_populates='amenities')
