#!/usr/bin/python3
"""
Place module
"""
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.amenity import Amenity

# Define the Many-to-Many relationship table
place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """
    Place class that inherits from BaseModel and Base.
    """
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    reviews = relationship("Review", backref="place",
                           cascade="all, delete, delete-orphan")
    amenities = relationship('Amenity', secondary=place_amenity,
                             viewonly=False, back_populates='place_amenities')

    @property
    def reviews(self):
        """
        Returns the list of Review instances with place_id
        equals to the current Place.id
        """
        from models import storage
        review_list = []
        for review in storage.all(Review).values():
            if review.place_id == self.id:
                review_list.append(review)
        return review_list

    @property
    def amenities(self):
        """
        Getter for amenities in FileStorage
        """
        from models import storage
        amenity_list = []
        for amenity in storage.all(Amenity).values():
            if amenity.id in self.amenity_ids:
                amenity_list.append(amenity)
        return amenity_list

    @amenities.setter
    def amenities(self, obj):
        """
        Setter for amenities in FileStorage
        """
        if type(obj) == Amenity:
            self.amenity_ids.append(obj.id)
