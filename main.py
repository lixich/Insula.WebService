#!flask/bin/python
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

def register_blueprints():
    from user import app_user
    from dose import app_dose
    from forecast import app_forecast
    app.register_blueprint(app_forecast, url_prefix='/forecast')
    app.register_blueprint(app_user, url_prefix='/user')
    app.register_blueprint(app_dose, url_prefix='/dose')

register_blueprints()

if __name__ == '__main__':
    app.run(host='192.168.0.100',debug = True, threaded=True)
