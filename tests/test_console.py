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


class TestHBNBCommand(unittest.TestCase):
    """
    Test cases for the HBNBCommand class.
    """

    def setUp(self):
        """
        Set up test environment.
        """
        storage._FileStorage__objects = {}
        self.console = HBNBCommand()

    def tearDown(self):
        """
        Clean up test environment.
        """
        storage._FileStorage__objects = {}

    def test_create(self):
        """
        Test create command for various models.
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.onecmd("create BaseModel")
            model_id = fake_out.getvalue().strip()
            self.assertIn(f"BaseModel.{model_id}", storage.all())

            self.console.onecmd("create User")
            user_id = fake_out.getvalue().strip().split('\n')[-1]
            self.assertIn(f"User.{user_id}", storage.all())

            self.console.onecmd("create State")
            state_id = fake_out.getvalue().strip().split('\n')[-1]
            self.assertIn(f"State.{state_id}", storage.all())

            self.console.onecmd("create City")
            city_id = fake_out.getvalue().strip().split('\n')[-1]
            self.assertIn(f"City.{city_id}", storage.all())

            self.console.onecmd("create Amenity")
            amenity_id = fake_out.getvalue().strip().split('\n')[-1]
            self.assertIn(f"Amenity.{amenity_id}", storage.all())

            self.console.onecmd("create Place")
            place_id = fake_out.getvalue().strip().split('\n')[-1]
            self.assertIn(f"Place.{place_id}", storage.all())

            self.console.onecmd("create Review")
            review_id = fake_out.getvalue().strip().split('\n')[-1]
            self.assertIn(f"Review.{review_id}", storage.all())

    def test_show(self):
        """
        Test show command for various models.
        """
        bm = BaseModel()
        bm.save()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.onecmd(f"show BaseModel {bm.id}")
            output = fake_out.getvalue().strip()
            self.assertIn(bm.id, output)

    def test_destroy(self):
        """
        Test destroy command for various models.
        """
        bm = BaseModel()
        bm.save()
        bm_id = bm.id
        self.assertIn(f"BaseModel.{bm_id}", storage.all())
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.onecmd(f"destroy BaseModel {bm_id}")
            self.assertNotIn(f"BaseModel.{bm_id}", storage.all())

    def test_all(self):
        """
        Test all command for various models.
        """
        bm = BaseModel()
        bm.save()
        user = User()
        user.save()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.onecmd("all")
            output = fake_out.getvalue().strip()
            self.assertIn(f"BaseModel.{bm.id}", output)
            self.assertIn(f"User.{user.id}", output)

    def test_update(self):
        """
        Test update command for various models.
        """
        bm = BaseModel()
        bm.save()
        bm_id = bm.id
        with patch('sys.stdout', new=StringIO()):
            self.console.onecmd(f"update BaseModel {bm_id} name 'Test'")
            self.assertEqual(storage.all()[f"BaseModel.{bm_id}"].name, 'Test')


if __name__ == '__main__':
    unittest.main()
