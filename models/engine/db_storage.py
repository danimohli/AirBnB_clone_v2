#!/usr/bin/python3
"""
DBStorage module
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base
from models.city import City
from models.state import State
from models.user import User
from models.place import Place


class DBStorage:
    """
    DBStorage class
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initialize the database
        """
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB),
                                      pool_pre_ping=True)
        if HBNB_ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query on the current database session
        """
        new_dict = {}
        if cls:
            for obj in self.__session.query(cls).all():
                key = obj.__class__.__name__ + '.' + obj.id
                new_dict[key] = obj
        else:
            for sub_cls in [State, City, User, Place]:
                for obj in self.__session.query(sub_cls).all():
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """
        Add the object to the current database session
        """
        self.__session.add(obj)

    def save(self):
        """
        Commit all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete from the current database session obj if not None
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Create all tables in the database and create the current
        database session
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
