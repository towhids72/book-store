import json

import sqlalchemy
from flask import Blueprint, request
from flask_login import login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from api_response.response import APIResponse
from user.models import User, db

user_blueprint = Blueprint('user_api_routes', __name__, url_prefix='/api/users')


@user_blueprint.route('/all', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    data = [user.serialize() for user in all_users]
    return APIResponse.ok_response(data=data)


@user_blueprint.route('/create', methods=['POST'])
def create_user():
    json_body = json.loads(request.data)
    username = json_body.get('username', None)
    password = json_body.get('password', None)
    if username is None:
        return APIResponse.error_response('username is missing')
    if password is None:
        return APIResponse.error_response('password is missing')
    try:
        user = User()
        user.username = username
        user.password = generate_password_hash(password, method='sha256')
        user.is_admin = False
        db.session.add(user)
        db.session.commit()
        return APIResponse.ok_response(user.serialize())
    except sqlalchemy.exc.IntegrityError:
        return APIResponse.error_response('user with the username already exist')


@user_blueprint.route('/login', methods=['POST'])
def login_user_request():
    json_body = json.loads(request.data)
    username = json_body.get('username', None)
    password = json_body.get('password', None)
    if username is None:
        return APIResponse.error_response('username is missing')
    if password is None:
        return APIResponse.error_response('password is missing')

    user = User.query.filter_by(username=username).first()
    if not user:
        return APIResponse.error_response('User with given username does not exist', 404)

    if not check_password_hash(user.password, password):
        return APIResponse.error_response('Password is not correct', 401)

    user.update_api_key()
    db.session.commit()
    login_user(user)
    return APIResponse.ok_response(user.serialize())


@user_blueprint.route('/logout', methods=['POST'])
def logout_user_request():
    if not current_user.is_authenticated:
        return APIResponse.error_response('User not logged in')
    logout_user()
    return APIResponse.ok_response(data=[], message='User logged out')


@user_blueprint.route('/<user_id>/details', methods=['GET'])
def get_user_info(user_id):
    if not current_user.is_authenticated:
        return APIResponse.error_response('Login to see your profile', 401)
    user = User.query.filter_by(id=user_id).first()
    if not user or current_user.id != int(user_id):
        return APIResponse.error_response('You don\'t have access to others profile', 401)
    return APIResponse.ok_response(user.serialize())
