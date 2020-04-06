from functools import wraps
from flask import request, jsonify
from os import environ


key = environ.get('SECRET_KEY')


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        elif 'x-access-tokens' in request.cookies:
            token = request.cookies['x-access-tokens']
        else:
            return jsonify({'message': 'a valid token is missing'})
        if token == key:
            return f(*args, **kwargs)
        else:
            return jsonify({'message': 'token is invalid'})
    return decorator