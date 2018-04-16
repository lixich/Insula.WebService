#!flask/bin/python
from flask import Flask, Blueprint, jsonify, abort, request, make_response
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app_user = Blueprint('', __name__)

user_set = [
    {
        'Id': 1,
        'Username': '1',
        'Password': '1'
    },
    {
        'Id': 2,
        'Username': '2',
        'Password': '2'
    }
]
dose_class = {
    'Id': int,
    'Username': str,
    'Password': str
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
