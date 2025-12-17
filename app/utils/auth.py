from jose import jwt
import jose
from datetime import datetime,timedelta,timezone
from flask import request, jsonify
from functools import wraps 

SECRET_KEY="super secret secrets"

def encode_token(customer_id, role='mechanic'):
    payload= {
        "exp": datetime.now(timezone.utc) + timedelta(days=0,hours=2),
        "iat": datetime.now(timezone.utc),
        "sub": str(customer_id),
        "role": role
    }
    token=jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
        if not token:
            return jsonify({'error': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jose.exceptions.JWTError:
            return jsonify({'error': 'Token is invalid!'}), 401
        except jose.exceptions.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired!'}), 401
        return f(*args, **kwargs)
    return decorated

def mechanic_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
        if not token:
            return jsonify({'error': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            if data.get('role') != 'mechanic':
                return jsonify({'error': 'Mechanic access required!'}), 403
            request.mechanic_id = int(data['sub'])
        except jose.exceptions.JWTError:
            return jsonify({'error': 'Token is invalid!'}), 401
        except jose.exceptions.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired!'}), 401
        # If the route already provided a mechanic_id (e.g. /mechanics/<id>),
        # avoid passing duplicates and ensure the token matches the path param.
        route_mechanic_id = kwargs.get('mechanic_id')
        if route_mechanic_id is not None and int(route_mechanic_id) != request.mechanic_id:
            return jsonify({'error': 'Forbidden'}), 403

        if route_mechanic_id is None:
            kwargs['mechanic_id'] = request.mechanic_id

        return f(*args, **kwargs)
    return decorated

def customer_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
        if not token:
            return jsonify({'error': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            if data.get('role') != 'customer':
                return jsonify({'error': 'Customer access required!'}), 403
            request.customer_id = int(data['sub'])
        except jose.exceptions.JWTError:
            return jsonify({'error': 'Token is invalid!'}), 401
        except jose.exceptions.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired!'}), 401
        # If the route already provided a customer_id (e.g. /customers/<id>),
        # avoid passing duplicates and ensure the token matches the path param.
        route_customer_id = kwargs.get('customer_id')
        if route_customer_id is not None and int(route_customer_id) != request.customer_id:
            return jsonify({'error': 'Forbidden'}), 403

        if route_customer_id is None:
            kwargs['customer_id'] = request.customer_id

        return f(*args, **kwargs)
    return decorated