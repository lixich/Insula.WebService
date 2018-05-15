from flask import Blueprint, jsonify, abort, request, url_for
from user import auth, get_user_id, get_current_user
from dose import dose_set
from algorithms import run_algorithms

app_forecast = Blueprint('forecast', __name__)

def average(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def average_alg(doses):
    values = [value['Insulin'] for value in doses]
    return round(average(values))

def zero_alg(doses):
    return 0

@app_forecast.route('/', methods = ['POST'])
@auth.login_required
def create_forecast():
    print(request.json)
    if not request.json:
        abort(400)
    user_doses = [dose for dose in dose_set if dose['UserId'] == get_user_id(auth.username())]
    forecasts = run_algorithms(request.json, user_doses)
    return jsonify(forecasts), 201
