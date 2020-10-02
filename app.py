import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from db import db
from resources.user import UserRegister, UserLogin, UserLogout, TokenRefresh, SetPassword
from resources.case import Case, CaseHistory
from blacklist import BLACKLIST

from models.status import StatusModel


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or ''
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

api = Api(app)
jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'error': 'token_expired',
        'description': 'The token has expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'error': 'invalid_token',
        'description': 'Signature verification failed'
        }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'error': 'authorization_required',
        'description': 'Request does not contain an access token.'
        }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'error': 'fresh_token_required',
        'description': 'The token is not fresh.'
        }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'error': 'token_revoked',
        'description': "The token has been revoked."
    })


@app.before_first_request
def create_tables():
    try:
        db.create_all()

        if not StatusModel.query.filter_by(name='New').first():
            statuses = ['New', 'Planned', 'In progress', 'Completed']
            for status in statuses:
                db.session.add(StatusModel(name=status))
            db.session.commit()
    except:
        # return {'message': 'Internal server error'}, 500
        pass


api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Case, '/case')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(SetPassword, '/change_password')
api.add_resource(CaseHistory, '/case_history')


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
