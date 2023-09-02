import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('xtopher','wolf','localhost:5432', self.database_name)
        self.app = create_app(test_config=self.database_path)
        self.client = self.app.test_client
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories_returns_success_and_categories(self):
        result = self.client().get('/categories')
        
        self.assertEqual( result.status_code, 200 )
        self.assertTrue('categories' in json.loads( result.data).keys())

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()