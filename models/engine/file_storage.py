#!/usr/bin/python3
"""
FileStorage class for managing storage of objects in JSON files.
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
    Serializes instances to a JSON file and deserializes
    JSON file to instances.
    """

    __file_path = 'file.json'
    __objects = {}

    def all(self):
        """
        Returns the dictionary __objects.
        """
        return self.__objects

    def new(self, obj):
        """
        Adds a new object to __objects.
        """
        self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj

    def save(self):
        """
        Serializes __objects to the JSON file.
        """
        with open(self.__file_path, 'w') as f:
            objs = {key: obj.to_dict() for key, obj in self.__objects.items()}
            json.dump(objs, f)

    def reload(self):
        """
        Deserializes the JSON file to __objects.
        """
        try:
            with open(self.__file_path, 'r') as f:
                objs = json.load(f)
                for obj in objs.values():
                    cls_name = obj['__class__']
                    self.new(eval(cls_name)(**obj))
        except FileNotFoundError:
            pass

    def close(self):
        """
        Calls reload() method to deserialize the JSON file to objects.
        """
        self.reload()
