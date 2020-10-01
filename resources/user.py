from flask_restful import Resource
from flask import request
from models.user import UserModel
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_refresh_token_required,
                                fresh_jwt_required,
                                get_jwt_identity,
                                jwt_required,
                                get_raw_jwt)
import bcrypt
from blacklist import BLACKLIST


class UserRegister(Resource):
    @classmethod
    def post(cls):
        """
        URL: http://{{server_url}}/register
        METHOD: POST

        Headers:
            Content-Type: application/json
        Input: {
            "username": "preferred username"
            "password": "preferred password"
        }
        :return: JSON of report message
        """
        data = request.get_json()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        password = bytes(data["password"], encoding='utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        user = UserModel(data['username'], hashed_password)
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class UserLogin(Resource):
    @classmethod
    def post(cls):
        """
        URL: http://{{server_url}}/login
        METHOD: POST

        Headers:
            Content-Type: application/json
        Input: {
            "username": "max length 80",
            "password": "max length 80"
        }
        :return: JSON of "access-" and "refresh-" tokens
        """
        data = request.get_json()
        user = UserModel.find_by_username(data['username'])
        password_from_request = bytes(data["password"], encoding='utf-8')

        if user and bcrypt.checkpw(password_from_request, bytes(user.password, encoding='utf-8')):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200

        return {'message': 'Invalid credentials'}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        """
        URL: http://{{server_url}}/logout
        METHOD: POST

        Headers:
            Authorization - "Bearer {{access_token}}"
        Input: {}

        :return: JSON of report message
        """
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message': 'Successfully logged out'}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        """
        URL: http://{{server_url}}/refresh
        METHOD: POST

        Headers:
            Content-Type: application/json
            Authorization - "Bearer {{access_token}}"
        Input: {}

        :return: JSON of a new access_token
        """
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200


class SetPassword(Resource):
    @classmethod
    @fresh_jwt_required
    def post(cls):
        """
        URL: http://{{server_url}}/change_password
        METHOD: POST

        Headers:
            Content-Type: application/json
            Authorization - "Bearer {{access_token}}"
        Input: {
            "username": "username of a current user",
            "new_password": "new required password"
        }

        :return: JSON of a new access_token
        """
        data = request.get_json()
        user = UserModel.find_by_username(data['username'])
        if not user:
            return {'message': 'User not found'}, 404

        password_from_request = bytes(data["new_password"], encoding='utf-8')
        hashed_password = bcrypt.hashpw(password_from_request, bcrypt.gensalt())
        user.password = hashed_password
        user.save_to_db()
        return {'message': 'User password updated'}, 201
