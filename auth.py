import json
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Response
)

from relatome.db import get_db

from .controllers import AuthController

bp = Blueprint('auth', __name__, url_prefix='/auth')
controller = AuthController()
SECRET_KEY = "secret"

@bp.route('/register', methods=['POST'])
def register():
    print("in register")
    print(request.data)
    data = json.loads(str(request.data, encoding='utf-8'))
    print(data)
    return controller.register(data)
    # return {}, 200

@bp.route('/login', methods=['POST'])
def login():
    data = json.loads(str(request.data, encoding='utf-8'))
    # session.permanent = True
    res = controller.login(data, session)
    print('in30')
    session['hello'] = 'World'
    print(session)
    return res

@bp.route('/logout', methods=['POST'])
def logout():
    print("in logout")
    print(session)
    return controller.logout(session)


@bp.route('/logged-in-user', methods=['GET', 'OPTIONS'])
def loggedInUser():
    return controller.loggedInUser(session)
