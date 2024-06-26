#!/usr/bin/python3
"""
Contains the User class
"""

import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String

STORAGE_TYPE = os.getenv('HBNB_TYPE_STORAGE')


class User(BaseModel, Base if STORAGE_TYPE == 'db' else object):
    """
    This class defines a user by various attributes
    """
     def __init__(self, *args, **kwargs):
        """
        initialize user
        """
        super().__init__(*args, **kwargs)
    
    if STORAGE_TYPE == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''
