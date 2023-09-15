# Trivia API

The Udacity Trivia API is a web application that allows users to play trivia games, manage questions, and search for questions based on different criteria. This project is part of the Full Stack Web Developer Nanodegree program at Udacity.

## Getting Started
To get started with the Udacity Trivia API, follow the instructions below.

### Prerequisites
Python 3.7 or higher
Flask
PostgreSQL

### Installation
1. Clone the repository:
    ```
    git clone https://github.com/your-username/udacity-trivia-api.git
    ```
1. Navigate to the project directory:
    ```
    cd udacity-trivia-api
    ```
1. Create a virtual environment:
    ```
    python3 -m venv venv
    ```
1. Activate the virtual environment:
    - For macOS/Linux:
    ```
    source venv/bin/activate
    ```
    - For Windows:
    ```
    venv\Scripts\activate
    ```
1. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```
1. Set up the database:
    - Create a PostgreSQL database named trivia:
    ```
    createdb trivia
    ```
    - Import the sample data into the database:
    ```
    psql trivia < trivia.psql
    ```
1. Start the server:
    ```
    export FLASK_APP=flaskr
    export FLASK_ENV=development
    flask run
    ```
## API Endpoints
The Udacity Trivia API provides the following endpoints:

* `GET /categories`: Retrieves a list of all available categories.
* `GET /questions`: Retrieves a paginated list of questions which can be filtered with a search parameter.
* `GET /questions/{question_id}`: Retrieves a single question specified by it's Id.
* `GET /categories/{category_id}/questions`: Retrieves a paginated list of questions in a specific category.
* `POST /questions`: Creates a new question.
* `DELETE /questions/{question_id}`: Deletes a question.
* `GET /quizzes`: Retrieves a random question for a quiz.

For detailed information about each endpoint, including request parameters and response bodies, please refer to the API Documentation section below.

## API Documentation
### GET /categories
Retrieves a list of all available categories.

**Request Parameters**: 
* None

**Response Body**: 
```
json { "categories": { "1": "Science", "2": "Art", "3": "Geography", "4": "History", "5": "Entertainment", "6": "Sports" }, "success": true }
```

### GET /questions
Retrieves a paginated list of questions. The set of questions in the result can be controlled with request parameters.

**Request Parameters**:
* `page` (optional): The page number to retrieve (default: 1).
* `q` (optional): A question search term. Only questions containing this search term in the question text are returned. 

**Response Body**: 
```
json { "categories": { "1": "Science", "2": "Art", "3": "Geography", "4": "History", "5": "Entertainment", "6": "Sports" }, "current_category": null, "questions": [ { "id": 1, "question": "What is the capital of France?", "answer": "Paris", "difficulty": 2, "category": 3 }, ... ], "success": true, "total_questions": 20 }
```

### GET /questions/{question_id}
Retrieves a single question by it's Id.

**Request Parameters**:
* None

**Response Body**: 
```
json { "question": { "id": 1, "question": "What is the capital of France?", "answer": "Paris", "difficulty": 2, "category": 3 }, "success": true }
```

### GET /categories/{category_id}/questions
Retrieves a paginated list of questions in a specific category.

**Request Parameters**:
* `page` (optional): The page number to retrieve (default: 1).

**Response Body**: 
```
json { "categories": { "1": "Science", "2": "Art", "3": "Geography", "4": "History", "5": "Entertainment", "6": "Sports" }, "current_category": "Science", "questions": [ { "id": 10, "question": "What is the chemical symbol for gold?", "answer": "Au", "difficulty": 3, "category": 1 }, ... ], "success": true, "total_questions": 5 }
```

### POST /questions
Creates a new question.

**Request Body**:
```
json { "question": "What is the capital of Italy?", "answer": "Rome", "difficulty": 2, "category": 3 }
```

**Response Body**: 
```
json { "question": { "id": 10, "question": "What is the chemical symbol for gold?", "answer": "Au", "difficulty": 3, "category": 1 }, "success": true }
```

### DELETE /questions/{question_id}
Deletes a question.

**Request Body**:
* `question_id`: The ID of the question to delete.

**Response Body**: 
```
json { "success": true }
```

### GET /quizzes
Retrieves a random question for a quiz.

**Request Parameters**:

* `category` (optional): the id of the category for the next question. If none is provided a random category is selected
* `previous_questions` (optional): a comma separated list of questions already used.


**Response Body**: 
```
json { "question": { "id": 4, "question": "What is the largest planet in our solar system?", "answer": "Jupiter", "difficulty": 2, "category": 1 }, "success": true }
```

## Testing
To run the tests for the Udacity Trivia API, execute the following command:

```
python -m unittest test_flaskr.py
```

## Author
Chris Brandt

## Acknowledgments
Udacity for providing the project idea and starter code.
License
This project is licensed under the MIT License.