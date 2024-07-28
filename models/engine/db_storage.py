#!/usr/bin/python3
"""
DBStorage class for managing storage of objects in a database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """
    Manages storage of objects in a SQL database.
    """

    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes a new DBStorage instance.
        """
        self.__engine = create_engine('mysql+mysqldb://user:password@localhost/dbname')
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))

    def all(self, cls=None):
        """
        Returns a dictionary of all objects of type cls,
        or all objects if cls is None.
        """
        if cls:
            objects = self.__session.query(cls).all()
        else:
            objects = self.__session.query(State).all() + \
                      self.__session.query(City).all() + \
                      self.__session.query(Amenity).all() + \
                      self.__session.query(Place).all() + \
                      self.__session.query(Review).all() + \
                      self.__session.query(User).all()
        return {obj.id: obj for obj in objects}

    def new(self, obj):
        """
        Adds a new object to the database session.
        """
        self.__session.add(obj)

    def save(self):
        """
        Commits the current database session.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes obj from the current database session.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Loads the database session.
        """
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))()

    def close(self):
        """
        Calls remove() method on the private session attribute.
        """
        self.__session.remove()
