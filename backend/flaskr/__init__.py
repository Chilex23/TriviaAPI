import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_cors import CORS
import random

from models import setup_db, Question, Category, Leaderboard

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/*": {"origin": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def all_categories():
        categories = Category.query.all()
        if len(categories) < 1:
            abort(404)
        
        return jsonify({
            "success": True,
            "categories": [category.format() for category in categories],
            "total_categories": len(categories)
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions")
    def get_questions():
        selection = Question.query.all()
        categories = Category.query.all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) < 1:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": len(selection),
                "categories": [category.format() for category in categories],
                "current_category": None
            }
        )

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)

        if question == None:
            abort(404)

        question.delete()
        return jsonify({
            "success": True,
            "deleted": question_id
        })

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        if body == None:
            abort(400)

        #get the json value if search term is in the json body
        if 'searchTerm' in body.keys():
            searchTerm = body.get('searchTerm', None)
            if searchTerm:
                selection = Question.query.filter(Question.question.ilike(f'%{searchTerm}%')).all()
                current_questions = paginate_questions(request, selection)
                if len(current_questions) < 1:
                    abort(404)
                return jsonify({
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(selection),
                    "current_category": None
                })
            else:
                abort(400)
        else:
            for key in ['question', 'answer', 'difficulty', 'category']:
                if key not in body.keys() or body[key] == None or body[key] == '':
                    abort(422)

            question = Question(
                question=body['question'],
                answer=body['answer'],
                difficulty=body['difficulty'],
                category=body['category'],
            )
            question.insert()

            return jsonify({
                "success": True,
                "created": question.format()
            })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_for_categoy(category_id):
        questions = Question.query.filter(
            Question.category == category_id).all()
        paginated_questions = paginate_questions(request, questions)

        if len(paginated_questions) < 1:
            return abort(404)

        return jsonify({
            "success": True,
            "questions": paginated_questions,
            "total_questions": len(questions),
            "current_category": category_id
        })


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
    @app.route("/quizzes", methods=["POST"])
    def get_question_for_quiz():
        body = request.get_json()
        previous_questions = body.get('previous_questions', None)
        category = body.get('quiz_category', None)
        if category == None:
            abort(400)
            
        if category['id'] == 0:
            questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
        else:
            questions = Question.query.filter(
                Question.category == category['id'],
                Question.id.notin_(previous_questions)).all()
        # No more questions return none to end the game
        if len(questions) < 1:
            return jsonify({
                "success": True,
                "question": None
            })
    
        question = random.choice(questions).format()

        return jsonify({
            "success": True,
            "question": question
        })

    @app.route("/leaderboard")
    def get_leaderboard_scores():
        ''' Endpoint to get leaderboard scores '''

        results = Leaderboard.query.order_by(desc(Leaderboard.score)).all()
        paginated_results = paginate_questions(request, results)
        return jsonify({
            "results": paginated_results,
            "totalResults": len(results)
        })

    @app.route("/leaderboard", methods=["POST"])
    def post_to_leaderboard():
        try:
            player = request.get_json()["name"]
            score = int(request.get_json()["score"])

            board_item = Leaderboard(player=player, score=score)
            board_item.insert()

            return jsonify({
                "added": board_item.id,
                "success": True
            })
        except Exception:
            abort(400)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )
    
    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(405)
    def not_allowed(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify({"success": False, "error": 500, "message": "internal server error"}),
            500,
        )

    return app

