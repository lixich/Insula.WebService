#!flask/bin/python
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

def register_blueprints():
    import user
    import dose
    app.register_blueprint(user.app_user, url_prefix='/')
    app.register_blueprint(dose.app_dose, url_prefix='/dose')

register_blueprints()

if __name__ == '__main__':
    app.run(debug = True)
