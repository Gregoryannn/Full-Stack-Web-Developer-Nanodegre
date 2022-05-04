# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

To activate a virtual environment in powershell:
```
name_of_virtual_environment\Scripts\activate
```

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

same in powershell

This will install all of the required packages we selected within the `requirements.txt` file.

Requirements folder updated to the following:
aniso8601==6.0.0
Click==7.0
Flask==1.1.2
Flask-Cors==3.0.7
Flask-RESTful==0.3.7
Flask-SQLAlchemy==2.4.4
itsdangerous==1.1.0
Jinja2==2.10.1
MarkupSafe==1.1.1
psycopg2-binary==2.8.6
pytz==2019.1
six==1.12.0
SQLAlchemy==1.3.20
Werkzeug==0.15.5

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```
If using powershell, the command is:
```
psql -U username -d trivia -f trivia.psql
```
## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
from powershell:
```powershell
$env:FLASK_APP = "__init__.py"
$
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT

This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

## Endpoints

## Categories

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
EXAMPLE:
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions'
- Fetches a dictionary of questions, total number of questions, list of categories, and current category.
- Results are paginated in groups of 10.
EXAMPLE:
{"categories":{"1":"Science","2":"Art","3":"Geography","4":"History","5":"Entertainment","6":"Sports"},"current_category":null,"questions":[{"answer":"Maya Angelou","category":4,"difficulty":2,"id":1,"question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"},{"answer":"Muhammad Ali","category":4,"difficulty":1,"id":2,"question":"What boxer's original name is Cassius Clay?"},{"answer":"Apollo 13","category":5,"difficulty":4,"id":3,"question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"},{"answer":"Tom Cruise","category":5,"difficulty":4,"id":4,"question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"},{"answer":"Edward Scissorhands","category":5,"difficulty":3,"id":5,"question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"},{"answer":"Brazil","category":6,"difficulty":3,"id":6,"question":"Which is the only team to play in every soccer World Cup tournament?"},{"answer":"Uruguay","category":6,"difficulty":4,"id":7,"question":"Which country won the first ever soccer World Cup in 1930?"},{"answer":"George Washington Carver","category":4,"difficulty":2,"id":8,"question":"Who invented Peanut Butter?"},{"answer":"Lake Victoria","category":3,"difficulty":2,"id":9,"question":"What is the largest lake in Africa?"},{"answer":"The Palace of Versailles","category":3,"difficulty":3,"id":10,"question":"In which royal palace would you find the Hall of Mirrors?"}],"success":true,"total_questions":20}

DELETE /questions/question_id/delete
- Deletes the question signified by the question id, if found. Returns question id and success message if found.
EXAMPLE:
{
    "success": True,
    "deleted": question_id,
}

POST /questions
- Creates a new question from the submitted question, answer, category, and difficulty values.
- Returns a success value and list of paginated questions.
EXAMPLE:
{
    "success": True,
    "questions": questions
}

POST /questions/search
- Searches for a question based on the query provided, returns a success value, a list of matching questions, and number of matching questions.

POST /quizzes
- Request body that checks for previously asked questions and returns a random question.


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
If done with powershell, use DROP DATABASE and CREATE DATABASE commands in psql, then exit to powershell and use the 
```powershell
psql -U username -d trivia -f trivia.psql
```
command to import trivia.psql into your local trivia database. Otherwise the steps are the same.