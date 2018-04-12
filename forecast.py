from flask import Blueprint, jsonify, abort, request, url_for
from user import auth, get_user_id
from dose import dose_set
from db import update_record, create_record

app_forecast = Blueprint('forecast', __name__)

def average(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def forecast_dose(doses):
    values = [value['Insulin'] for value in doses]
    return round(average(values))

def make_public_forecast(forecast):
    new_forecast = {}
    for field in forecast:
        if field == 'Id':
            new_forecast['uri'] = url_for('dose.get_dose', dose_id = forecast['Id'], _external = True)
        else:
            new_forecast[field] = forecast[field]
    return new_forecast

@app_forecast.route('/', methods = ['POST'])
@auth.login_required
def create_forecast():
    if not request.json:
        abort(400)
    user_doses = [dose for dose in dose_set if dose['UserId'] == get_user_id(auth.username())]
    forecast = {'Forecast': forecast_dose(user_doses)}
    return jsonify( { 'forecast': make_public_forecast(forecast) } ), 201
