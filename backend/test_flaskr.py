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
    Categories
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
        
    """
    GET Questions
    """
        
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
    
    def test_get_questions_non_existant_page_returns_an_empty_set(self):
        get_result = self.client().get('/questions?page=99999')
        
        get_result_json = json.loads( get_result.data )
        
        self.assertEqual( get_result.status_code, 200 )
        self.check_basic_response_format( get_result, ['questions'] )
        
        self.assertEqual(len(get_result_json['questions']), 0, 'Requesting a non-existant page of questions should return an empty page.')
        
    def test_get_questions_without_category_sets_current_category_to_a_valid_category(self):
        result = self.client().get('/questions')
        
        data_json = json.loads( result.data )
        
        self.check_basic_response_format( result, ['categories', 'questions', 'current_category', 'total_questions'] )
        
        current_category = data_json['current_category']
        self.assertNotEqual( current_category, None, 'Incorrect response format. Current category is set to None')

    def test_get_a_question_by_id_returns_a_question(self):
        get_result = self.client().get(f'/questions/1')
        self.check_basic_response_format(get_result, ['question'])

    def test_get_of_non_existant_question_results_in_404(self):
        get_result = self.client().get(f'/questions/10000')
        
        self.check_basic_response_format(get_result)
        get_data_json = json.loads(get_result.data)
 
        self.assertEqual(get_result.status_code, 404, 'Get of a non-existant question should return a 404.')
        self.assertEqual(get_data_json['error'], 404, 'Incorrect response message. Get of a non-existant question should return a 404')

    def test_get_with_a_search_term_returns_those_questions(self):
        get_result = self.client().get('/questions?q=Tim Burton')
        
        self.assertEqual( get_result.status_code, 200, 'Get questions with a search term returned an error.')
        self.check_basic_response_format(get_result, ['categories', 'questions', 'current_category', 'total_questions'])
        
        get_result_json = json.loads(get_result.data)
        
        self.assertEqual(len(get_result_json['questions']), 1, 'Get questions with "Tim Burton" should return 1 question')

    def test_get_with_a_search_term_and_a_page_returns_the_correct_page(self):
        get_result = self.client().get('/questions?q=in&page=2')
        
        self.assertEqual( get_result.status_code, 200, 'Get questions with a search term returned an error.')
        self.check_basic_response_format(get_result, ['categories', 'questions', 'current_category', 'total_questions'])
        
        get_result_json = json.loads(get_result.data)
        
        self.assertGreater(len(get_result_json['questions']), 1, 'Get questions searching for 'in' with page 2 should return more than 1 question')
    
    def test_get_questions_with_category_gets_only_those_questions(self):
        questions_read = 0
        page = 1
        get_all_result = self.client().get(f'/questions?page={page}')
        get_all_result_json = json.loads(get_all_result.data)
        science_questions = [question for question in get_all_result_json['questions'] if question['category']==1 ]
        total_questions = get_all_result_json['total_questions']
        while questions_read < total_questions:
            questions_read += len(get_all_result_json['questions'])
            page += 1
            get_all_result = self.client().get(f'/questions?page={page}')
            get_all_result_json = json.loads(get_all_result.data)
            new_science_questions = [question for question in get_all_result_json['questions'] if question['category']==1 ]
            science_questions.extend(new_science_questions)
            
        
        get_science_questions_result = self.client().get('/categories/1/questions')
        get_science_questions_json = json.loads(get_science_questions_result.data)
        
        self.check_basic_response_format( get_science_questions_result, ['categories', 'questions', 'current_category', 'total_questions'])
        self.assertEqual(len(science_questions), len(get_science_questions_json['questions']), 'Get questions by category should have the same number of questions as those from the full set with that category')
        i = 0
        for question in science_questions:
            self.assertDictEqual(question, get_science_questions_json['questions'][i])
            i += 1

    """
    GET Quizzes
    """        
    def test_get_quizzes_with_no_parameters_returns_a_question(self):
        get_result = self.client().get('/quizzes')
        
        get_result_json = json.loads(get_result.data)
        
        self.check_basic_response_format(get_result, ['question', 'success'])
        self.assertTrue(get_result_json['success'], 'Get Quizzes with no parameters should return successfully')
        self.assertIn('question', get_result_json['question'], 'Get Quizzes should return a dictionary with a question key')
    
    def test_get_quizzes_with_a_valid_category_returns_a_question_in_that_category(self):
        get_result = self.client().get('/quizzes?category=1')
        
        get_result_json = json.loads(get_result.data)
        
        self.check_basic_response_format(get_result, ['question', 'success'])
        self.assertTrue(get_result_json['success'], 'Get Quizzes with a valid category should return successfully')
        self.assertIn('category', get_result_json['question'], 'Get Quizzes should return a dictionary with a category key')
        self.assertEqual( get_result_json['question']['category'], 1, 'Get Quizzes should return a question in the same category as requested')
        
    def test_get_quizzes_with_an_invalid_category_returns_no_question(self):
        get_result = self.client().get('/quizzes?category=9999')
        
        get_result_json = json.loads(get_result.data)
        
        self.check_basic_response_format(get_result, ['success'])
        self.assertTrue(get_result_json['success'], 'Get Quizzes with an invalid category should return successfully')
        self.assertNotIn('question', get_result_json, 'Get Quizzes should not return a question key when no question can be found')
            
    def test_get_quizzes_with_no_questions_left_returns_no_question(self):
        get_result = self.client().get('/quizzes?category=1&previous_questions=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23')
        
        get_result_json = json.loads(get_result.data)
        
        self.check_basic_response_format(get_result, ['success'])
        self.assertTrue(get_result_json['success'], 'Get Quizzes with an invalid category should return successfully')
        self.assertNotIn('question', get_result_json, 'Get Quizzes should not return a question key when no question can be found')
    """
    DELETE Questions
    """
        
    def test_delete_question_removes_the_question(self):
        get_result = self.client().get('/questions')
        
        get_data_json = json.loads( get_result.data )
        first_question = get_data_json['questions'][0]
        delete_result = self.client().delete(f'/questions/{first_question["id"]}')
        self.check_basic_response_format(delete_result)
        self.assertEqual(delete_result.status_code, 200, 'Delete of a valid question resulted in an error.')
        
        get_result_2 = self.client().get('/questions')
        
        get_data_json_2 = json.loads( get_result_2.data )
        questions = get_data_json_2['questions']
        deleted_question = [question for question in questions if question['id']==first_question['id'] ]
        self.assertEqual( len(deleted_question), 0, f"The question with id {first_question['id']} was not deleted.")
        
    def test_delete_of_non_existant_question_results_in_404(self):
        delete_result = self.client().delete(f'/questions/10000')
        
        self.check_basic_response_format(delete_result)
        delete_data_json = json.loads(delete_result.data)
 
        self.assertEqual(delete_result.status_code, 404, 'Delete of a non-existant question should return a 404.')
        self.assertEqual(delete_data_json['error'], 404, 'Incorrect response message. Delete of a non-existant question should return a 404')

    """
    POST Questions
    """
    def test_post_question_adds_a_qustion(self):
        new_question = {'question': 'Why do we write our tests first?',
                        'answer': 'So that we only satify those tests.',
                        'category': '1',
                        'difficulty': '2'}
        
        post_result = self.client().post('/questions', json=new_question)
        
        self.check_basic_response_format(post_result, ['question'])
        self.assertEqual(post_result.status_code, 200, 'Posting a valid question resulted in an error')
        post_result_json = json.loads(post_result.data)
        self.assertEqual(new_question['question'], post_result_json['question']['question'], 'The question returned after posting a new question should be the same question.')
        
        get_result = self.client().get(f'/questions/{post_result_json["question"]["id"]}')
        get_result_json = json.loads(get_result.data)
        self.assertDictEqual(post_result_json['question'], get_result_json['question'] )
        
    def test_posting_an_incomplete_question_results_in_a_400(self):
        new_question = {'question': 'Why do we write our tests first?',
                        'answer': 'So that we only satify those tests.'}
        
        post_result = self.client().post('/questions', json=new_question)
        
        self.check_basic_response_format(post_result)
        self.assertEqual(post_result.status_code, 400, 'Posting an invalid question should result in an error')
        
             
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()