#!flask/bin/python
from flask import Flask, Blueprint, jsonify, abort, request, make_response
from flask_httpauth import HTTPBasicAuth
from db import update_record, create_record

auth = HTTPBasicAuth()
app_user = Blueprint('', __name__)

user_set = [
    {
        'Id': 1,
        'Username': '1',
        'Password': '1',
        'Birthday': '1.01.2000',
        'Weight': 40,
        'Growth': 160,
        'Insulin': 'Название',
        'NormalGlucose': 5.0
    },
    {
        'Id': 2,
        'Username': '2',
        'Password': '2',
        'Birthday': '1.07.1990',
        'Weight': 60,
        'Growth': 175,
        'Insulin': 'Регуляр',
        'NormalGlucose': 4.5
    }
]
user_class = {
    'Id': int,
    'Username': str,
    'Password': str,
    'Birthday': str,
    'Weight': float,
    'Growth': float,
    'Insulin': int,
    'NormalGlucose': float
}

def get_user_id(username):
    users = [user for user in user_set if user['Username'] == username]
    if len(users) == 0:
        return None
    return users[0]['Id']

@app_user.route('/', methods = ['GET'])
@auth.login_required
def login_required():
    if auth.username():
        users = [user for user in user_set if user['Username'] == auth.username()]
        return jsonify(users[0]), 201
    else:
        return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app_user.route('/', methods = ['POST'])
def create_user():
    if not request.json:
        abort(400)
    user = { 'Id': user_set[-1]['Id'] + 1 if len(user_set) else 1 }
    if not create_record(user_class, request, user):
        abort(400)
    user_set.append(user)
    return jsonify(user), 201

@auth.get_password
def get_password(username):
    users = [user for user in user_set if user['Username'] == username]
    if len(users) == 0:
        return None
    return users[0]['Password']

@app_user.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app_user.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)
