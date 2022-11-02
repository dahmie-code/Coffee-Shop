from crypt import methods
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
    Initialize the datbase
'''
db_drop_and_create_all()

# ROUTES
'''
    GET /drinks
'''

@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.order_by(Drink.id).all()
    print(drinks)
    
    drinks_format = [drink.short() for drink in drinks]
    
    return jsonify({
        'success': True,
        'drinks': drinks_format
    }), 200

'''
    GET /drinks-detail
'''

@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    drinks = Drink.query.order_by(Drink.id).all()
    print(drinks)
    
    drinks_format = [drink.long() for drink in drinks]
    
    return jsonify({
        'success': True,
        'drinks': drinks_format
    }), 200
    
'''
    POST /drinks
'''

@app.route('/drinks-detail', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(payload):
    body = request.get_json()
    recipe = body['recipe']
    title = body['title']
    
    if not ('title' in body and 'recipe' in body):
        abort(422)
    
    new_drink = Drink(title=title, recipe=json.dumps(recipe))
    drink_format = [drink.long() for drink in drinks]
    try:
        new_drink.insert()
        drinks = Drink.query.all()
        print(drinks)
    except:
        abort(422)
    return jsonify({
        'success': True,
        'drinks': drink_format
    }), 200
    
'''
    PATCH /drinks/<id>
'''

@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drink(payload, id):
    drink = Drink.query.get(id)
    body = request.get_json()
    title = body.get('title')
    recipe = body.get('recipe')
    
    if drink is None:
        abort(404)
    try:
        if title is not None:
            drink.title = title
        if recipe is not None:
            drink.recipe = json.dumps(recipe)
        drink.update()
           
        
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except:
        abort(404)
'''
DELETE /drinks/<id>
'''
@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    drink = Drink.query.get(id)
    print(drink)
    
    if drink is None:
        abort(400)
    try:
        drink.delete()
    except:
        abort(404)
    return jsonify({
        'success': True,
        'drinks': id
    })



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

"""Error handling for bad request entity"""
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
    }), 400

"""Error handling for Resource not found entity"""

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

"""Error handling for AuthError entity"""
@app.errorhandler(AuthError)
def auth_error(e):
    return jsonify({
        "success": False,
        "error": e.status_code,
        "message": e.error
    }), e.status_code