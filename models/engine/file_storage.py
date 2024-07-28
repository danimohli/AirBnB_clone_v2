#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """
    Serializes instances to a JSON file and deserializes JSON file to instances
    """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of models currently in storage.
        If cls is specified, returns only instances of cls.
        """
        if cls:
            if isinstance(cls, str):
                cls = eval(cls)
            return {key: value for key, value in self.__objects.items()
                    if isinstance(value, cls)}
        return self.__objects

    def new(self, obj):
        """
        Adds a new object to the storage dictionary
        """
        self.__objects[obj.__class__.__name__ + '.' + obj.id] = obj

    def save(self):
        """
        Saves the storage dictionary to file
        """
        with open(self.__file_path, 'w') as f:
            temp = {}
            temp.update(self.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """
        Loads the storage dictionary from file
        """
        try:
            with open(self.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    cls_name = val["__class__"]
                    del val["__class__"]
                    self.__objects[key] = eval(cls_name)(**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it's inside
        """
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]
                self.save()

    def close(self):
        """
        Call reload() method for deserializing the JSON file to objects
        """
        self.reload()
