import os
import unittest
import json
from flask import request
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
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "postgres", "snowwhite01", "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": 'Who was the first President of Nigeria?',
            "answer": "Nnamdi Azikwe",
            "difficulty": 2,
            "category": 4
        }

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
    def test_get_paginated_questions_success(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data['categories'])
        self.assertIsNone(data['current_category'])

    def test_get_paginated_questions_error_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['total_categories'])

    def test_get_questions_based_on_category_success(self):
        category_id = 1
        res = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], category_id)

    def test_get_questions_for_category_error_no_results(self):
        category_id = 1000
        response = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_questions_for_category_question_page_exist_beyond_valid_range_error(self):
        category_id = 1
        response = self.client().get(f'/categories/{category_id}/questions?page=10000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_deleted_question_success(self):
        question = Question.query.order_by(Question.id.desc()).first()
        question_id = question.id

        response = self.client().delete(f'/questions/{question_id}')
        data = json.loads(response.data)

        question = Question.query.get(question_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)
        self.assertIsNone(question)

    def test_delete_question_error_question_not_exist(self):
        question_id = 100000000
        response = self.client().delete(f'/questions/{question_id}')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_created_question_success(self):
        response = self.client().post('/questions', json=self.new_question)
        data = json.loads(response.data)

        new_question = Question.query.order_by(Question.id.desc()).first()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertEqual(data['created']['id'], new_question.id)
        self.assertEqual(data['created']['question'], new_question.question)
        self.assertEqual(data['created']['answer'], new_question.answer)
        self.assertEqual(data['created']['difficulty'], new_question.difficulty)
        self.assertEqual(data['created']['category'], new_question.category)
    
    def test_create_question_bad_body_error(self):
        request = None

        response = self.client().post('/questions', json=request)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
    
    def test_create_question_question_is_missing_error(self):
        request = self.new_question.copy()
        del request["question"]

        response = self.client().post('/questions', json=request)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_question_question_is_empty_error(self):
        request = self.new_question.copy()
        request["question"] = ''

        response = self.client().post('/questions', json=request)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_question_answer_is_missing_error(self):
        request = self.new_question.copy()
        del request["answer"]

        response = self.client().post('/questions', json=request)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_question_answer_is_empty_error(self):
        request = self.new_question.copy()
        request["answer"] = ''

        response = self.client().post('/questions', json=request)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_question_difficulty_is_missing_error(self):
        request = self.new_question.copy()
        del request["difficulty"]

        response = self.client().post('/questions', json=request)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_question_category_is_missing_error(self):
        request = self.new_question.copy()
        del request["category"]

        response = self.client().post('/questions', json=request)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()