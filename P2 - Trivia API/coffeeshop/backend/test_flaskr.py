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
        self.database_path = "postgres://postgres:postgres@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

       # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
        #Sample question(s) for testing:
        self.question = {
            'test question': 'When did a NHL team from a Canadian city win the Stanley Cup?',
            'answer': '1993, Montreal Canadiens',
            'difficulty': '2',
            'category': 6
        }
        self.question2 = {
            'test_question2': '',
            'answer2': '',
            'difficulty': '',
            'category': ''
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

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'] > 0)

    def test_delete_question(self):
        res = self.client().delete('/questions/{}'.format(testQ.id))
        data = json.loads(res.data)
        res = self.client().delete('/questions/1')

        self.assertEqual(res.status_code, 200)

    def test_create_question(self):
        result = self.client().post('/questions', json=self.question)
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        def test_search_question(self):
        request_data = { 'searchTerm': 'Stanley Cup'}

        response = self.client().post('/questions/search', json=request_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['questions'], False)
        self.assertEqual(data['total_questions'], 1)

    #error handlers

    def test_404_get_questions(self):
        res = self.client().get('/questions?page=1993')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_422_question_post(self):
        res = self.client().post('/questions', json=self.question2)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main() 