import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from Flask import Flask, request, abort, jsonify
from Flask_SQLAlchemy import SQLAlchemy
from Flask_Cors import CORS
import random

from models import setup_db, Question, Category
QUESTIONS_PER_PAGE = 10
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

  CORS(app, resources={'/': {'origins': '*'}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  @DONE: Use the after_request decorator to set Access-Control-Allow
  '''

  @app.after_request
  def after_request(response):
    response.headers.add(
      'Access-Control-Allow-Headers',
      'Content-Type, Authorization, true'
    )
    response.headers.add(
      'Access-Control-Allow-Methods',
      'GET, POST, PATCH, DELETE, OPTIONS'
    )
    return response
  '''
  
  @Done: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()
    categories_dict = {}
    for category in categories:
      categories_dict[category.id] = category.type

      if (len(categories_dict)==0):
        abort(404)
      return jsonify({
        'success': True,
        'categories': categories_dict
      })

  '''
  @TODO: 
  @DONE: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  app.route('/questions')
  def get_questions():
    questions = Question.query.order_by(Question.id).all()
    total_questions = len(questions)
    categories = Category.query.order_by(Category.id).all()

    current_questions = get_paginated_questions(request, questions, QUESTIONS_PER_PAGE)

    if (len(current_questions) == 0):
      abort(404)

    categories_dict = {}
    for category in categories:
      categories_dict[category.id] = category.type 

    return jsonify({
      'success': True,
      'total_questions': total_questions,
      'categories': categories_dict,
      'questions': current_questions
    })
  '''
  @TODO: 
  @Done: 
  Create an endpoint to DELETE question using a question ID. 
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  '''
  @TODO: 
  @app.route('/questions/<int:id>', methods=[DELETE])
  def delete_question(id):
    try:
      question = Question.query.get(id)
      question.delete()
      return jsonify({
        'success': True,
      })
    except:
      abort(404)
  '''
  @DONE?: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.
  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''

  @app.route('/questions', methods=['POST'])
  def create_question():
    data = request.get_json()
    question = data.get('question', '')
    answer = data.get('answer', '')
    difficulty = data.get('difficulty', '')
    category = data.get('category', '')

    if (question == '') or (answer == '') or (difficulty == '') or (category == ''):
      abort(404)

    try:
      question = Question(
        question=question,
        answer=answer,
        difficulty=difficulty,
        category=category
      )
      question.insert()

      return jsonify({
        'success': True
      })

    except Exception:
      abort(404)
  '''
  @TODO?: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 
  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    data = request.get_json()
    search_term = data.get('searchTerm', '')
    if search_term == '':
      abort(404)

    try:
      questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

      if len(questions)==0:
        abort(404)

      paginated_questions = get_paginated_questions(request, questions, QUESTIONS_PER_PAGE)

      return jsonify({
        'success': True,
        'questions': paginated_questions,
        'total_questions': len(Question.query.all())
      })

    except Exception:
      abort(404)
  '''

  Create a GET endpoint to get questions based on category. 
  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions')
  def get_questions_by_category(id):
    category = Category.query.filter_by(id=id).one_or_none()

    if (category is None):
      abort(404)

    questions = Question.query.filter_by(category=id).all()

    paginated_questions = get_paginated_questions(request, questions, QUESTIONS_PER_PAGE)

    return jsonify({
      'success': True,
      'questions': paginated_questions,
      'total_questions': len(questions),
      'current_category': category.type
    })

  '''
  
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 
  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app