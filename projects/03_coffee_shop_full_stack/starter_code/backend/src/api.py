import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
     where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        get_drinks = Drink.query.all()
        return jsonify({
            'success': True,
            'drinks': [drink.short() for drink in get_drinks]
        }), 200
    except Exception as ex:
        abort(400)


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} 
    where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    try:
        get_drinks = Drink.query.all()

        return jsonify({
            'success': True,
            'drinks': [drink.long() for drink in get_drinks]
        }), 200
    except Exception as ex:
        abort(400)


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} 
    where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(payload):
    try:
        if request.data:
            get_body = request.get_json()
            get_title = get_body.get('title', None)
            get_recipe = get_body.get('recipe', None)
            drink = Drink(title=get_title, recipe=json.dumps(get_recipe))
            Drink.insert(drink)

            added_drink = Drink.query.filter_by(id=drink.id).first()

            return jsonify({
                'success': True,
                'drinks': [added_drink.long()]
            })
        else:
            abort(400)
    except Exception as ex:
        abort(422)


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} 
    where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    get_drink = Drink.query.get(id)
    if get_drink:
        try:
            get_body = request.get_json()
            title = get_body.get('title')
            recipe = get_body.get('recipe')
            if title:
                get_drink.title = title
            if recipe:
                get_drink.title = recipe
            get_drink.update()
            return jsonify({
                'success': True,
                'drinks': [get_drink.long()]
            }), 200
        except Exception as ex:
            abort(422)
    else:
        abort(404)


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} 
    where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks/<id>", methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    drink_to_be_deleted = Drink.query.get(id)
    if drink_to_be_deleted:
        try:
            drink_to_be_deleted.delete()
            return jsonify({
                'success': True,
                'delete': id
            }), 200
        except Exception as ex:
            abort(422)
    else:
        abort(404)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not found"
    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''


@app.errorhandler(AuthError)
def handle_auth_error(e):
    return jsonify({
        "success": False,
        "error": e.status_code,
        'message': e.error
    }), 401


@app.errorhandler(400)
def Bad_Request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request"
    }), 400


@app.errorhandler(500)
def Internal_Server_Error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error"
    }), 500


@app.errorhandler(405)
def Method_Not_Allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method Not Allowed"
    }), 405


@app.errorhandler(401)
def Unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401
