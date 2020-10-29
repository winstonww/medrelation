from pathlib import Path
print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())
import os
from flask import Flask
from flask_cors import CORS
from flask_session import Session


# creat_app naming is application specific, renaming this will not work
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, support_credentials=True)
    app.secret_key = 'secret'
    app.config.from_mapping(
        # SERVER_NAME='127.0.0.1:5000',
        # SESSION_COOKIE_NAME='127.0.0.1:5000',
        # SESSION_COOKIE_DOMAIN='127.0.0.1:5000',
        SESSION_COOKIE_SAMESITE="None",
        SESSION_COOKIE_SECURE=True,
        SESSION_TYPE='filesystem',
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, "relatome.sqlite"))
    Session(app)
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello_world():
        return "Hello World"

    @app.after_request
    def after_request(response):
      response.headers.add('Access-Control-Allow-Headers',
                           "Origin, X-Requested-With, Content-Type, Accept, x-auth")
      response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8080')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
      response.headers.add('Access-Control-Allow-Credentials', 'true')
      return response

    from . import db
    db.init_app(app)

    from . import api
    app.register_blueprint(api.bp)

    from . import auth
    app.register_blueprint(auth.bp)


    # associates endpoint index with '/'
    app.add_url_rule('/', endpoint='index')

    return app
