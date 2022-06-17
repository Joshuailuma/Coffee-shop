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
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True,
    "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks')
def drinks():
    try:
        # Query drinks
        drinks = Drink.query.all()
        # If drink has data
        if drinks:
            # Loop over drinks and return drink.short()
            for drink in drinks:
                drink_list = drink.short()
            return jsonify({
                "success": True,
                "drinks": drink_list
            }), 200
        else:
            # If no drink, return error
            return jsonify({
                "success": False,
                "error": 'No drink found'
            }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "error": e
        }), 422


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks":
    drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail', endpoint='drinks_detail')
@requires_auth('get:drinks-detail')
def drinks_detail(f):
    try:
        drinks = Drink.query.all()

        if drinks:
            for drink in drinks:
                drink_list = [drink.long()]

            return jsonify({
                "success": True,
                "drinks": drink_list
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": 'No drink found'
            }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "error": e
        }), 422


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True,
    "drinks": drink} where drink an array containing only
    the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'], endpoint='post_drinks')
@requires_auth('post:drinks')
def drinks(f):
    # Get data from the request
    body = request.form or request.json or request.data
    title = body.get('title')
    recipe_body = body.get('recipe')
    # If recipie is a string
    if recipe_body == str:
        recipe = recipe_body
    else:
        # if it isn't, convert it to a
        recipe = json.dumps(recipe_body)

    drink = Drink(title=title, recipe=recipe)
    # Insert into database
    try:
        drink.insert()
        return jsonify({
            'success': True,
            'drink': drink.long()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': e
        }), 422


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True,
    "drinks": drink} where drink an array containing only
    the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<id>', methods=['PATCH'], endpoint='patch_drinks')
@requires_auth('patch:drinks')
def drinks(f, id):

    try:
        # Get data from the body and make a query
        body = request.form or request.json or request.data
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if not drink:
            return jsonify({
                "success": False,
                "error": 'No drink of that id found'
            }), 404
        else:
            title = body.get('title')
            recipe_body = body.get('recipe')
            if recipe_body == str:
                recipe = recipe_body
            else:
                recipe = json.dumps(recipe_body)

            drink.title = title
            drink.recipe = recipe
            drink.update()
            return jsonify({
                'success': True,
                'drinks': [drink.long()]
            }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': e
        }), 422


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True,
    "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<id>', methods=['DELETE'], endpoint='delete_drinks')
@requires_auth('delete:drinks')
def drinks(f, id):
    try:
        # Get data from from input and query database
        body = request.form or request.json or request.data
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        # If no data exist
        if not drink:
            return jsonify({
                "success": False,
                "error": 'No drink of that id could be found'
            }), 404
        else:
            # If it exists
            # Delete data from database
            drink.delete()
            return jsonify({
                "success": True,
                "delete": id
            }), 200
    # If there's a problem trying all these
    except Exception as e:
        return jsonify({
            'success': False,
            'error': e
            }), 422


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
        "message": "resource not found"
    }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Check the request body"
    }), 400


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(AuthError)
def auth_error(err):
    response = jsonify(err.error)
    response.status_code = err.status_code
    return response
