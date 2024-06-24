#!/usr/bin/python3
"""
Contains the class TestHBNBCommand
"""

import unittest
from unittest.mock import patch
from io import StringIO
import os
import models
from models import storage
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from console import HBNBCommand


class TestHBNBCommand(unittest.TestCase):
    """Class to test the HBNBCommand functionality"""

    def setUp(self):
        """Set up test environment"""
        pass

    def tearDown(self):
        """Clean up after test"""
        pass

    @classmethod
    def setUpClass(cls):
        """Set up class-level fixtures"""
        cls.console = HBNBCommand()

    def test_pep8_conformance_console(self):
        """Test that console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_console(self):
        """Test that tests/test_console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_console_module_docstring(self):
        """Test for the console.py module docstring"""
        self.assertIsNot(console.__doc__, None,
                         "console.py needs a docstring")
        self.assertTrue(len(console.__doc__) >= 1,
                        "console.py needs a docstring")

    def test_HBNBCommand_class_docstring(self):
        """Test for the HBNBCommand class docstring"""
        self.assertIsNot(HBNBCommand.__doc__, None,
                         "HBNBCommand class needs a docstring")
        self.assertTrue(len(HBNBCommand.__doc__) >= 1,
                        "HBNBCommand class needs a docstring")

    def test_create(self):
        """Test create command for BaseModel"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create BaseModel')
            self.assertRegex(f.getvalue(), r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}')
            new_id = f.getvalue().strip()
            self.assertIn(f"BaseModel.{new_id}", storage.all())

    def test_show(self):
        """Test show command for BaseModel"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create BaseModel')
            new_id = f.getvalue().strip()
            self.console.onecmd(f'show BaseModel {new_id}')
            output = f.getvalue().split('\n')[1].strip()
            self.assertIn(f"BaseModel.{new_id}", output)

    def test_destroy(self):
        """Test destroy command for BaseModel"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create BaseModel')
            new_id = f.getvalue().strip()
            self.console.onecmd(f'destroy BaseModel {new_id}')
            self.assertNotIn(f"BaseModel.{new_id}", storage.all())

    def test_all(self):
        """Test all command for BaseModel"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create BaseModel')
            self.console.onecmd('all BaseModel')
            output = f.getvalue().split('\n')[1].strip()
            self.assertIn('BaseModel', output)

    def test_update(self):
        """Test update command for BaseModel"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create BaseModel')
            new_id = f.getvalue().strip()
            self.console.onecmd(f'update BaseModel {new_id} name "MyModel"')
            self.console.onecmd(f'show BaseModel {new_id}')
            output = f.getvalue().split('\n')[1].strip()
            self.assertIn('MyModel', output)

    @unittest.skipIf(type(models.storage) == FileStorage, "FileStorage
                     doesn't support MySQL testing")
    def test_mysql_create_state(self):
        """Test creating a State in MySQL"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State name="California"')
            new_id = f.getvalue().strip()
            self.assertRegex(new_id, r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}')

            # Assuming DBStorage, test MySQL interaction
            db_connection = models.storage._DBStorage__session.connection()
            result = db_connection.execute('SELECT COUNT(*) FROM states')
            count = result.fetchone()[0]
            self.assertEqual(count, 1)


if __name__ == '__main__':
    unittest.main()
