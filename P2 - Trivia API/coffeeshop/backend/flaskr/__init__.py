import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import Column, String, Integer, create_engine
import json

database_name = "trivia"
database_path = "postgresql://peter:postgres@{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
Question
'''
class Question(db.Model):  
  __tablename__ = 'questions'

  id = Column(Integer, primary_key=True)
  question = Column(String)
  answer = Column(String)
  category = Column(String)
  difficulty = Column(Integer)

  def __init__(self, question, answer, category, difficulty):
    self.question = question
    self.answer = answer
    self.category = category
    self.difficulty = difficulty

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'question': self.question,
      'answer': self.answer,
      'category': self.category,
      'difficulty': self.difficulty
    }

'''
Category
'''
class Category(db.Model):  
  __tablename__ = 'categories'

  id = Column(Integer, primary_key=True)
  type = Column(String)

  def __init__(self, type):
    self.type = type

  def format(self):
    return {
      'id': self.id,
      'type': self.type
    }

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)
  '''
  @DONE: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add(
      'Access-Control-Allow-Headers',
      'Content-Type, Authorization'
    )
    response.headers.add(
      'Access-Control-Allow-Methods',
      'GET, POST, PUT, DELETE'
    )
    return response
  # Helper function to paginate questions
    
  def get_paginated_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
      
    return current_questions
  '''
  @Done: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
      categories = Category.query.all()
      if len(categories) == 0:
        abort(404)
      return jsonify({
        'success': True,
        'categories': {category.id: category.type for category in categories}
      })
  '''
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
  app.route('/questions', methods=['GET'])
  def get_questions():
    selection = Question.query.order_by(Question.id).all()
    current_questions = get_paginated_questions(request, selection)
    categories = Category.query.order_by(Category.type).all()
    
    if (len(current_questions) == 0):
      abort(404)
    
    return jsonify({
      'success': True,
      'total_questions': len(selection),
      'questions': current_questions,
      'categories': {category.id: category.type for category in categories},
      'current_category': None,
    })
  '''
  @Done: 
  Create an endpoint to DELETE question using a question ID. 
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question_to_delete = Question.query.get(question_id)
      question_to_delete.delete()
      return jsonify({
        'success': True,
        'deleted': question_id,
      })
    except:
      abort(422)
      
  '''
  @DONE?: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.
  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    data = request.get_json()
    
    create_question = data.get('question')
    create_answer = data.get('answer')
    create_difficulty = data.get('difficulty')
    create_category = data.get('category')
    if (create_question == '') or (create_answer == '') or (create_difficulty == '') or (create_category == ''):
      abort(422)
    try:
      question = Question(
        question=create_question,
        answer=create_answer,
        difficulty=create_difficulty,
        category=create_category
      )
      question.insert()
      return jsonify({
        'success': True,
        'question created': question.id,
      })
    except:
      abort(422)
  '''
  @TODO?: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 
  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    data = request.get_json()
    search_term = data.get('searchTerm')
    try:
      selection = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
      paginated_questions = get_paginated_questions(request, selection)
      return jsonify({
        'success': True,
        'questions': paginated_questions,
        'total_questions': len(selection),
        'current_category': None,
      })
    except:
      abort(404)
  '''
  @TODO?: 
  Create a GET endpoint to get questions based on category. 
  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):
    try:  
      selection = Question.filter(Question.category == str(category_id)).all()
      paginated_questions = get_paginated_questions(request, selection)
      
      return jsonify({
        'success': True,
        'questions': paginated_questions,
        'total_questions': len(selection),
        'current_category': category_id,
      })
    
    except:
      abort(404)
  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 
  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quiz_question():
    try:
      data = request.get_json()
      previous_questions = data.get('previous_questions')
      q_category = data.get('quiz_category')
      if ((q_category is None) or (previous_questions is None)):
        abort(422)
      if (q_category['id'] == 0):
        questions = Question.query.all()
      else:
        questions = Question.query.filter_by(category=q_category['id']).all()
      def get_random_question():
        return questions[random.randint(0, len(questions) - 1)]
      next_question = get_random_question
      found = True
      while found:
        if next_question.id in previous_questions:
          next_question = get_random_question()
        else:
          found = False
      return jsonify({
        'success': True,
        'question': next_question
      })
    except:
      abort(422)
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'Bad request error'
    }), 400
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'Resource not found'
    }), 404
  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': 'Method not allowed'
    }), 405
  @app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'Unprocessable entity'
    }), 422
  return app    