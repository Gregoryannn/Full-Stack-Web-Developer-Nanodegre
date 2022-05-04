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
        self.database_path = "postgresql://peter:postgres@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

     #Sample question(s) for testing:
        self.new_question = {
            'question': '"When did a NHL team from a Canadian city win the Stanley Cup?"',
            'answer': '1993, Montreal Canadiens',
            'category': 6,
            'difficulty': 2
        }
        self.new_question2 = {
            'question': '',
            'answer': '',
            'category': '',
            'difficulty': ''
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])

    def test_fail_to_get_categories(self):
        res = self.client().get('/categories/7')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'] > 0)
    
    def test_fail_to_get_questions(self):
        res = self.client().get('/questions/1993')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
    
    def test_get_questions_in_category(self):
        res = self.client().get('/categories/1993/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete_question(self):
        res = self.client().delete('/questions/17')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_fail_to_delete_question(self):
        res = self.client().delete('/questions/1993')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_create_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_search_question(self):
        res = self.client().post('/questions/search', json={'search_term': 'NHL team from a Canadian city'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_failed_search_question(self):
        res = self.client().post('/questions/search', json={'search_term': ' '})
        data = json.loads(res.data)

        self.assertTrue(data['total_questions'] == 0)

    def test_get_quiz(self):
        res = self.client().post('/quizzes', json={'previous_questions': [], \
                                                   'quiz_category': {'id': '6', 'type': 'Sports'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])

    def test_fail_to_get_quiz(self):
        res = self.client().post('/quizzes', json={'previous_questions': [], \
                                                   'quiz_category': {'id': '1993', 'type': 'Canadian'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)

    #error handlers
    
    def test_404_get_questions_per_category(self):
        res = self.client().get('/categories/7/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_405_add_questions_to_category(self):
        res = self.client().post('/categories/2/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)

    def test_422_question_post(self):
        res = self.client().post('/questions', json=self.new_question2)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()