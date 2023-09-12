import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def filter_questions(request):
    search_term = request.args.get("q", '', type=str)
    return Question.question.like(f'%{search_term}%')

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    with app.app_context():
        if test_config is None:
            setup_db(app)
        else:
            setup_db(app, test_config)

    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    
    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        categories_json_formated = {}
        for category in categories:
            categories_json_formated[category.id] = category.type
        return jsonify({
            "categories": categories_json_formated, 
            "success": True
        })
    

    @app.route('/questions', methods=['GET'])
    def get_questions_no_page_specified():
        filter_criteria = filter_questions(request)
        questions = Question.query.filter(filter_criteria).order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)
        categories = Category.query.all()
        categories_json_formated = {}
        for category in categories:
            categories_json_formated[category.id] = category.type
        
        return jsonify({
            "categories": categories_json_formated,
            "questions": current_questions,
            "current_category": categories_json_formated[1],
            "total_questions": len(questions),
            "success": True
        })

    @app.route('/questions/<int:question_id>', methods=['GET'])
    def get_question_by_id(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()
        
        if question is None:
            abort(404)
        else:
            return jsonify({
                'question': question.format(),
                'success': True
            })
        
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_question_by_category(category_id):
        
        questions = Question.query.filter(Question.category == str( category_id )).all()
        current_questions = paginate_questions(request, questions)
        categories = Category.query.all()
        categories_json_formated = {}
        for category in categories:
            categories_json_formated[category.id] = category.type
            
        return jsonify({
            'categories': categories_json_formated,
            'current_category': categories_json_formated[category.id],
            'questions': current_questions,
            'success': True,
            'total_questions': len(questions)
        })
            
            
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question_to_delete = Question.query.filter(Question.id == question_id).one_or_none()
        
        if question_to_delete is None:
            abort(404)
        else:
            try:
                question_to_delete.delete()
            except:
                abort(500)
        
        return jsonify({
            'success': True
        })
                

    @app.route('/questions', methods=['POST'])
    def post_question():
        data = request.get_json()
        
        if 'question' not in data or 'answer' not in data or 'category' not in data or 'difficulty' not in data:
            abort(400)
        
        question = Question(
            question=data['question'],
            answer=data['answer'],
            category=data['category'],
            difficulty=int(data['difficulty'])
        )
        
        try:
            question.insert()
        except:
            abort(500)
            
        return jsonify({
            'question': question.format(),
            'success': True
        })
        

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def handle_resource_not_found(self):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found.'
        }), 404
        
    @app.errorhandler(405)
    def handle_method_not_allowed(self):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method not allowed.'
        }), 405
        
        
    
    @app.errorhandler(400)
    def handle_bad_request(error):
        return jsonify({
            "success": False, 
            "error": 400, 
            "message": "bad request"
        }), 400
    
    @app.errorhandler(500)
    def handle_server_error(error):
        return jsonify({
            "success": False, 
            "error": 500, 
            "message": "Server error."
        }), 500
        
    return app

