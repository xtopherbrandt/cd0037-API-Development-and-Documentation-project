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

    def check_basic_response_format(self, result, response_keys = [] ):
        
        result_data_json = json.loads( result.data )
        self.assertTrue('success' in result_data_json.keys(), 'Incorrect response format. Missing "success" key' )       

        if int( result.status_code / 100 ) == 2 :
            self.assertEqual( result_data_json['success'], True, f'Incorrect response message. Status code == {result.status_code}, response message not True' ) 
            for key in response_keys:
                self.assertIn( key, result_data_json, f'Incorrect response message. Missing the key: {key}' )
        else:
            self.assertEqual( result_data_json['success'], False, f'Incorrect response message. Status code == {result.status_code}, response message not False' )
            self.assertEqual( result_data_json['error'], result.status_code, f'HTTP response status code {result.status_code} does not match response message error code {result_data_json["error"]}')
            self.assertIn('message', result_data_json, 'Incorrect response message, missing error message')
        return
            
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories_returns_all_categories(self):
        result = self.client().get('/categories')
        
        data_json = json.loads( result.data )
                
        self.assertEqual( result.status_code, 200 )
        self.check_basic_response_format( result, ['categories'] )
        self.assertGreater( len(data_json['categories']), 0 )
        
    def test_categories_are_returned_in_correct_format(self):
        result = self.client().get('/categories')
        
        data_json = json.loads( result.data )
                
        self.assertEqual( result.status_code, 200 )
        self.check_basic_response_format( result, ['categories'] )
        self.assertEqual( type(data_json['categories']), dict, "Incorrect response format. GET Categories did not return a dict.")

    def test_get_categories_returns_method_not_allowed_for_POST(self):
        result = self.client().post('/categories')
        self.assertEqual( result.status_code, 405 )
        self.check_basic_response_format( result )
        
    def test_get_questions_without_page_returns_first_page_of_questions(self):
        result = self.client().get('/questions')
        
        self.assertEqual( result.status_code, 200 )
        self.check_basic_response_format( result, ['categories', 'questions', 'current_category', 'total_questions'] )
        
        questions_returned_no_page_number = json.loads( result.data )['questions']
        
        result_2 = self.client().get('/questions?page=1')
        questions_returned_page_1 = json.loads( result_2.data )['questions']
        
        question_index = 0
        for question_no_page in questions_returned_no_page_number:
            question_page_1 = questions_returned_page_1[question_index]
            self.assertDictEqual(question_no_page, question_page_1, 'GET questions without a page query did not return the same set as GET questions with a page query')
            question_index += 1

    def test_get_questions_page_2_returns_a_set_of_questions_after_page_1(self):
        result_2 = self.client().get('/questions?page=2')
        
        data_json_2 = json.loads( result_2.data )
        
        self.assertEqual( result_2.status_code, 200 )
        self.check_basic_response_format( result_2, ['questions'] )
        
        id_of_first_question = data_json_2['questions'][0]['id']
        
        result_1 = self.client().get('/questions?page=1')
        data_json_1 = json.loads( result_1.data )
        id_of_last_question = data_json_1['questions'][-1]['id']
        
        self.assertGreater(id_of_first_question, id_of_last_question, 'First question of second page is not greater than last question of first page.')

    def test_get_questions_without_category_sets_current_category_to_a_valid_category(self):
        result = self.client().get('/questions')
        
        data_json = json.loads( result.data )
        
        self.assertEqual( result.status_code, 200 )
        self.check_basic_response_format( result, ['categories', 'questions', 'current_category', 'total_questions'] )
        
        current_category = data_json['current_category']
        self.assertNotEqual( current_category, None, 'Incorrect response format. Current category is set to None')
        
    def test_delete_question_removes_the_question(self):
        get_result = self.client().get('/questions')
        
        get_data_json = json.loads( get_result.data )
        first_question = get_data_json['questions'][0]
        delete_result = self.client().delete(f'/questions/{first_question["id"]}')
        delete_data_json = json.loads(delete_result.data)
        self.assertIn('success', delete_data_json, 'Incorrect response format. Missing success key.')
        self.assertTrue(delete_data_json['success'], 'Delete of the first question did not return a success response.')
        
        get_result_2 = self.client().get('/questions')
        
        get_data_json_2 = json.loads( get_result_2.data )
        questions = get_data_json_2['questions']
        deleted_question = [question for question in questions if question['id']==first_question['id'] ]
        self.assertEqual( len(deleted_question), 0, f"The question with id {first_question['id']} was not deleted.")
        
    def test_delete_of_non_existant_question_results_in_404(self):
        delete_result = self.client().delete(f'/questions/10000')
        
        delete_data_json = json.loads(delete_result.data)
        self.assertIn('success', delete_data_json, 'Incorrect response format. Missing success key.')
        self.assertFalse(delete_data_json['success'], 'Delete of a non-existant question returned success = True.')
        self.assertEqual(delete_result.status_code, 404, 'Delete of a non-existant question should return a 404.')
        self.assertEqual(delete_data_json['error'], 404, 'Incorrect response message. Delete of a non-existant question should return a 404')
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()