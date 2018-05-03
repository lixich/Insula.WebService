from flask import Blueprint, jsonify, abort, request, url_for
from user import auth, get_user_id
from db import update_record, create_record
import pandas as pd
from datetime import datetime

app_dose = Blueprint('dose', __name__)
dose_set = [
    {
        'Id': 1,
        'Insulin': 4,
        'Time': '10:00',
        'Carbo': 5,
        'GlucoseBefore': 5.9,
        'GlucoseAfter': 6.2,
        'UserId': 1
    },
    {
        'Id': 2,
        'Insulin': 6,
        'Time': '12:00',
        'Carbo': 4,
        'GlucoseBefore': 3.5,
        'GlucoseAfter': 4.9,
        'UserId': 1
    }
]
dose_class = {
    'Id': int,
    'Insulin': float,
    'Time': str,
    'Carbo': float,
    'GlucoseBefore': float,
    'GlucoseAfter': float,
    'UserId': int
}

def make_public_dose(dose):
    new_dose = {}
    for field in dose:
        new_dose[field] = dose[field]
        if field == 'Id':
            new_dose['uri'] = url_for('dose.get_dose', dose_id = dose['Id'], _external = True)
    return new_dose

@app_dose.route('/', methods = ['GET'])
@auth.login_required
def get_dose_set():
    doses = [dose for dose in dose_set if dose['UserId'] == get_user_id(auth.username())]
    #return make_response(dumps(list(map(make_public_dose, doses))))
    return jsonify(list(map(make_public_dose, doses)))

@app_dose.route('/<int:dose_id>', methods = ['GET'])
@auth.login_required
def get_dose(dose_id):
    doses = [dose for dose in dose_set if dose['Id'] == dose_id]
    if len(doses) == 0:
        abort(404)
    return jsonify(make_public_dose(doses[0]))

@app_dose.route('/', methods=['POST'])
@auth.login_required
def create_dose():
    if not request.json:
        abort(400)
    dose = { 'Id': dose_set[-1]['Id'] + 1 if len(dose_set) else 1 }
    dose['UserId'] = get_user_id(auth.username())
    if not create_record(dose_class, request, dose):
        abort(400)
    dose_set.append(dose)
    return jsonify( make_public_dose(dose)), 201

@app_dose.route('/<int:dose_id>', methods=['PUT'])
@auth.login_required
def update_dose(dose_id):
    doses = [dose for dose in dose_set if dose['Id'] == dose_id]
    if len(doses) == 0 or not request.json:
        abort(404)
    dose = doses[0]
    update_record(dose_class, request, dose)
    return jsonify( make_public_dose(dose))

@app_dose.route('/<int:dose_id>', methods=['DELETE'])
@auth.login_required
def delete_dose(dose_id):
    doses = [dose for dose in dose_set if dose['Id'] == dose_id]
    if len(doses) == 0:
        abort(404)
    dose_set.remove(doses[0])
    return jsonify({'Result': True})

def load_data():
    global dose_set
    df = pd.read_excel('dataset.xlsx')
    df['Id'] = df.index
    df['Time'] = list(map(lambda x: datetime.strptime(x,'%d.%m.%Y %H:%M:%S'), df['Time']))
    dose_set = df.to_dict(orient='records')

load_data()
