from functools import wraps
from flask import jsonify, request, current_app
from flask_jwt_extended import (
      create_access_token, create_refresh_token, 
      jwt_required,get_jwt_identity, get_jwt, get_jti)
from pypipet.core.model.user import User
from pypipet.core.operations.user import register_new_user, find_users
from pypipet.api.api_blueprint import APIBlueprint
from pypipet.api.controllers.utility import get_session
from .identity import BLACKLIST, JTI_MAP
authBP = APIBlueprint('auth', __name__)


def validate_access(access_level):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # verify_jwt_in_request()
            user = get_jwt_identity()
            if user['access_level'] == 1 \
                or user['access_level'] == access_level:
                return fn(*args, **kwargs)
            else:
                return jsonify({
                     'message': 'not autherized'
                }), 403
            

        return decorator

    return wrapper    

def _verify_input(data, access_level=False):
    if data.get('username') is None:
        return 
    if data.get('password') is None:
        return
    if access_level and data.get('access_level') is None:
        return
    return data

@authBP.route('/register', methods=['POST'])
@jwt_required()
@validate_access(1)
def new_user():
    data =  request.get_json()
    if _verify_input(data, access_level=True) is None:
        return jsonify({
            'message': 'invalid user info'
            }), 403

    ctx = current_app.config['app_context']
    tables = ctx.get_table_objects()
    session = get_session(ctx)
    
    exist_users = find_users(tables.get('login_user'), session, {
        'username': data['username']
    })
    if exist_users is not None:
        session.close()
        return jsonify({
            'message': 'User {} already exists'.format(data['username'])
            }), 405
    
    access_level =  data.get('access_level', 0)
    new_user = User(
        {'username': data['username'],
        'password': User.generate_hash(data['password']),
        'access_level':access_level}
    )
    
    created = register_new_user(tables, session, new_user)
    if created is None:
        session.close()
        return jsonify({
            'message': 'creating User {} failed'.format(data['username'])
        }), 400

    identity_data = {'username': data['username'],
                        'access_level': access_level}
    access_token = create_access_token(identity = identity_data)
    refresh_token = create_refresh_token(identity = identity_data)
    session.close()
    return jsonify({
        'message': 'User {} was created'.format(data['username']),
        'access_token': access_token,
        'refresh_token': refresh_token
        }), 200
        
@authBP.route('/login', methods=['POST'])
def login():
    data =  request.get_json()
    if _verify_input(data) is None:
        return jsonify({
            'message': 'invalid user info'
            }), 403
    ctx = current_app.config['app_context']
    tables = ctx.get_table_objects()
    session = get_session(ctx)

    exist_users = find_users(tables.get('login_user'), session, {
        'username': data['username']
    })
    if exist_users is None:
        session.close()
        return jsonify({
            'message': 'user does not exist'
        }), 404
    
    user = User(exist_users[0])

    if user.verify_hash(data['password'], user.get_attr('password')):
        identity_data = {'username': data['username'],
                        'access_level': user.get_attr('access_level')}
        access_token = create_access_token(identity=identity_data, fresh=True)
        refresh_token = create_refresh_token(identity=identity_data)
        session.close()
        return jsonify({
            'message': 'User {} was created'.format(data['username']),
            'access_token': access_token,
            'refresh_token': refresh_token
            }), 200

    session.close()
    return jsonify({
        'message': 'authentication failed'
    }), 403


# for security, refresh may be disabled
@authBP.route('/refresh', methods=['POST'])
@jwt_required(refresh=True) 
def refresh_token():
    identity_data = get_jwt_identity()

    #only use once
    jti = get_jwt()['jti']
    BLACKLIST.add(jti)

    #revoke previous token
    jtis = JTI_MAP.get(identity_data['username'])
    if jtis is not None:
        for jti in list(jtis):
            BLACKLIST.add(jti)
        del JTI_MAP[identity_data['username']]
    
    access_token = create_access_token(identity=identity_data, fresh=False)
    return jsonify({
            'access_token': access_token,
            'message': 'refresh token'
            }), 200

@authBP.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    BLACKLIST.add(jti)
    
    data =  request.get_json()
    if data and data.get('refresh_token'):
        r_jti = get_jti(data['refresh_token'])
        BLACKLIST.add(r_jti)
    
    identity_data = get_jwt_identity()
    if JTI_MAP.get(identity_data['username']) is not None:
        del JTI_MAP[identity_data['username']]

    return jsonify({
        'message': 'successfully logged out'
    }), 200