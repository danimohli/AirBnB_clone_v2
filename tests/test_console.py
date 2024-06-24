#!/usr/bin/python3
"""
Comment for test module
"""
import unittest
from console import HBNBCommand
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import os


class TestHBNBCommand(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.cli = HBNBCommand()

    def tearDown(self):
        """Tear down test environment"""
        storage.all().clear()
        if os.path.exists('file.json'):
            os.remove('file.json')

    def test_create_with_string_param(self):
        self.cli.onecmd('create User name="John_Doe"')
        users = storage.all().values()
        self.assertEqual(len(users), 1)
        user = list(users)[0]
        self.assertEqual(user.name, "John Doe")

    def test_create_with_int_param(self):
        self.cli.onecmd('create Place number_rooms=3')
        places = storage.all().values()
        self.assertEqual(len(places), 1)
        place = list(places)[0]
        self.assertEqual(place.number_rooms, 3)

    def test_create_with_float_param(self):
        self.cli.onecmd('create Place latitude=37.7749')
        places = storage.all().values()
        self.assertEqual(len(places), 1)
        place = list(places)[0]
        self.assertEqual(place.latitude, 37.7749)

    def test_create_with_multiple_params(self):
        self.cli.onecmd('create State name="California"
                        capital="Sacramento" population=39538223')
        states = storage.all().values()
        self.assertEqual(len(states), 1)
        state = list(states)[0]
        self.assertEqual(state.name, "California")
        self.assertEqual(state.capital, "Sacramento")
        self.assertEqual(state.population, 39538223)

    def test_create_invalid_class(self):
        self.cli.onecmd('create InvalidClass name="test"')
        self.assertEqual(len(storage.all()), 0)

    def test_create_missing_class(self):
        self.cli.onecmd('create')
        self.assertEqual(len(storage.all()), 0)


if __name__ == '__main__':
    unittest.main()
