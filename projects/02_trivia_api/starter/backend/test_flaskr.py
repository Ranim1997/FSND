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
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://postgres:ranim1997@{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    '''
    A GET request to /questions endpoint returns a list of questions,
    number of total questions, current category, and categories.
    '''

    def test_200_get_paginated_questions(self):
        response_object = self.client().get('/questions')
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['questions'])
        self.assertTrue(response_data['total_questions'])
        self.assertTrue(response_data['categories'])

    '''
    A request for a non-existed question should return 404 status code.
    '''

    def test_404_get_paginated_questions(self):
        response_object = self.client().get('/questions?page=12345')
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 404)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['error'], 404)
        self.assertEqual(response_data['message'], "Not found")

    '''
    A GET request to /categories endpoint should return 
    a list of categories and number of categories.
    '''

    def test_200_get_categories(self):
        response_object = self.client().get('/categories')
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['categories'])
        self.assertTrue(response_data['number_of_categories'])

    '''
    A GET request to /categories/id/questions endpoint should return 
    a list of questions within specific category, total questions, and current category.
    '''

    def test_200_get_category_by_ID(self):
        response_object = self.client().get('/categories/1/questions')
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['questions'])
        self.assertTrue(response_data['total_questions'])
        self.assertTrue(response_data['current_category'])

    '''
    A request for a non-existed category should return 404 status code.
    '''

    def test_404_get_category_by_ID(self):
        response_object = self.client().get('/categories/123/questions')
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 404)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['error'], 404)
        self.assertEqual(response_data['message'], "Not found")

    '''
    A POST request to /questions endpoint should return 
    a list of questions within specific search term.
    '''

    def test_200_get_questions_by_searchterm(self):
        response_object = self.client().post(
            "/questions", json={"searchTerm": "name"})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['questions'])
        self.assertTrue(response_data['total_questions'])
        self.assertEqual(response_data['current_category'], None)

    '''
    A request for a non-existed search term should return 404 status code.
    '''

    def test_404_get_questions_by_searchterm(self):
        response_object = self.client().post(
            "/questions", json={"searchTerm": "ranimalmuslim"})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 404)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['error'], 404)
        self.assertEqual(response_data['message'], "Not found")

    '''
    A POST request to /post/questions endpoint should return 
    a status code 200.
    '''

    def test_200_post_new_question(self):
        response_object = self.client().post('/post/questions',
                                             json={"question": "Thank you?",
                                                   "answer": "You r welcome",
                                                   "category": 3, 
                                                   "difficulty": 2})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['message'])
    '''
    A POST request to /post/questions endpoint with missing required parameters
    should return a status code 400.
    '''

    def test_400_post_new_question(self):
        response_object = self.client().post('/post/questions',
                                             json={"question": "",
                                                   "answer": "",
                                                   "category": None})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 400)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'Bad Request')

    '''
    A DELETE request to /questions/id with given question ID should return a 200
    status code and delete the question from the database.
    '''
    
    def test_200_delete_question_by_id(self):

        response_object = self.client().delete("/questions/10")
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertTrue(response_data['message'])
    
    '''
    A DELETE request to /questions/id with a non-existed ID should return a 400.
    '''

    def test_400_delete_non_existed_question(self):
        response_object = self.client().delete("/questions/123456")
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 400)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'Bad Request')

    '''
    A POST request to /quizzes get the next question of the quiz should return a random question
    within the given category, which is not included in the list of previous questions.
    '''

    def test_200_play_quiz(self):

        payload = {"previous_questions": [],
                   "quiz_category": {"id": 2}}
        response_object = self.client().post('/quizzes', json=payload)
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        question_from_endpoint = response_data['question']

    '''
    A POST request to /quizzes without specifying the quiz category correctly
    should return 400 status code.
    '''

    def test_400_play_quiz(self):

        payload = {"previous_questions": {},
                   "quiz_category": {'id': None}}

        response_object = self.client().post('/quizzes', json=payload)
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 400)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'Bad Request')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
