#!flask/bin/python
from flask import Flask, Blueprint, jsonify, abort, request, make_response
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app_user = Blueprint('', __name__)

user_set = [
    {
        'Id': 1,
        'UserName': '1',
        'Password': '1'
    },
    {
        'Id': 2,
        'UserName': '2',
        'Password': '2'
    }
]
dose_class = {
    'Id': int,
    'UserName': str,
    'Password': str
}

def get_user_id(username):
    users = [user for user in user_set if user['UserName'] == username]
    if len(users) == 0:
        return None
    return users[0]['Id']

@auth.get_password
def get_password(username):
    users = [user for user in user_set if user['UserName'] == username]
    if len(users) == 0:
        return None
    return users[0]['Password']

@app_user.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app_user.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)
