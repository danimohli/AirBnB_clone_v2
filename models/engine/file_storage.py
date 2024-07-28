#!/usr/bin/python3
"""
This module defines the FileStorage class which handles serialization and
deserialization of instances to and from JSON files.
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """
    Handles storage of all class instances in a JSON file.
    """

    # String - path to the JSON file
    __file_path = "file.json"
    # Dictionary - will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """
        Returns the dictionary __objects, optionally filtered by cls.
        """
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """
        Sets obj in __objects with key <obj class name>.id.
        """
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path).
        """
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """
        Deserializes the JSON file to __objects.
        """
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it's inside.
        """
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """
        Calls reload() method for deserializing the JSON file to objects.
        """
        self.reload()
