#!flask/bin/python
from flask import Flask, Blueprint, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth
from db import update_record, create_record

auth = HTTPBasicAuth()
app_user = Blueprint('', __name__)

user_set = [
    {
        'Id': 1,
        'Username': '1',
        'Password': '1',
        'Birthday': '1.04.1996',
        'Weight': 50,
        'Growth': 177,
        'Insulin': 'Регуляр',
        'NormalGlucose': 6.0
    },
    {
        'Id': 2,
        'Username': '2',
        'Password': '2',
        'Birthday': '1.07.1984',
        'Weight': 50,
        'Growth': 175,
        'Insulin': 'Хумалог',
        'NormalGlucose': 6.0
    },
    {
        'Id': 3,
        'Username': '3',
        'Password': '3',
        'Birthday': '1.03.1995',
        'Weight': 65,
        'Growth': 178,
        'Insulin': 'Хумалог',
        'NormalGlucose': 6.0
    },
    {
        'Id': 4,
        'Username': '4',
        'Password': '4',
        'Birthday': '1.03.1990',
        'Weight': 60,
        'Growth': 175,
        'Insulin': 'Регуляр',
        'NormalGlucose': 6.0
    },
    {
        'Id': 5,
        'Username': '5',
        'Password': '5',
        'Birthday': '1.03.1965',
        'Weight': 49,
        'Growth': 169,
        'Insulin': 'Хумалог',
        'NormalGlucose': 6.0
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

def make_public_user(user):
    new_user = {}
    for field in user:
        new_user[field] = user[field]
        if field == 'Id':
            new_user['uri'] = url_for('.get_user', user_id = user['Id'], _external = True)
    return new_user

def get_user_id(username):
    users = [user for user in user_set if user['Username'] == username]
    if len(users) == 0:
        return None
    return users[0]['Id']

def get_current_user():
    users = [user for user in user_set if user['Username'] == auth.username()]
    if len(users) == 0:
        return None
    return users[0]

@app_user.route('/', methods = ['GET'])
@auth.login_required
def login_required():
    if auth.username():
        users = [user for user in user_set if user['Username'] == auth.username()]
        return jsonify(make_public_user(users[0])), 201
    else:
        return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app_user.route('/<int:user_id>', methods = ['GET'])
@auth.login_required
def get_user(user_id):
    users = [user for user in user_set if user['Id'] == user_id]
    current_user = get_current_user()
    if len(users) == 0 or get_current_user()['Id'] != user_id:
        abort(404)
    return jsonify(make_public_user(users[0]))

@app_user.route('/', methods = ['POST'])
def create_user():
    if not request.json:
        abort(400)
    user = { 'Id': user_set[-1]['Id'] + 1 if len(user_set) else 1 }
    if not create_record(user_class, request, user):
        abort(400)
    user_set.append(user)
    return jsonify(make_public_user(user)), 201

@app_user.route('/<int:user_id>', methods=['PUT'])
@auth.login_required
def update_dose(user_id):
    users = [dose for dose in user_set if dose['Id'] == user_id]
    if len(users) == 0 or not request.json:
        abort(404)
    user = users[0]
    update_record(user_class, request, user)
    return jsonify( make_public_user(user))

@auth.get_password
def get_password(username):
    users = [user for user in user_set if user['Username'] == username]
    if len(users) == 0:
        return None
    return users[0]['Password']

@app_user.route('/<int:user_id>', methods=['DELETE'])
@auth.login_required
def delete_user(user_id):
    users = [user for user in user_set if user['Id'] == user_id]
    if len(users) == 0:
        abort(404)
    user_set.remove(users[0])
    return jsonify({'Result': True})
