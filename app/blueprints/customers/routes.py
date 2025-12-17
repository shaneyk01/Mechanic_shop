from flask import Flask,jsonify,request
from marshmallow import ValidationError 
from sqlalchemy import select
from . import customers_bp
from .schemas import customer_schema, customers_schema, login_schema
from app.models import Customer, ServiceTickets, db
from app.extensions import limiter
from app.utils.auth import encode_token, customer_token_required
from app.blueprints.serviceTickets.schemas import service_tickets_schema


@customers_bp.route('/login', methods=['POST'])
def login():
    try:
        creds = login_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    query = select(Customer).where(Customer.email == creds['email'])
    customer = db.session.execute(query).scalars().first()

    if customer and customer.password == creds['password']:
        token = encode_token(customer.id, role='customer')
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401


@customers_bp.route('/', methods=['POST'])
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    query = select(Customer).where(Customer.email == customer_data['email'])
    existing_customer = db.session.execute(query).scalars().all()
                
    if existing_customer:
        return jsonify({'message': 'Customer with this email already exists.'}), 400

    new_customer = Customer(**customer_data)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

@customers_bp.route('/',methods=['GET'])
def get_customers():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        query = select(Customer)
        customers = db.paginate(query, page=page, per_page=per_page)
        return jsonify({
            'data': customers_schema.dump(customers.items),
            'total': customers.total,
            'pages': customers.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
    except:
        query = select(Customer)
        customers = db.session.execute(query).scalars().all()
        return jsonify(customers_schema.dump(customers)), 200
    
 

@customers_bp.route('/<int:customer_id>',methods=['GET'])
def get_a_customer(customer_id):
    customer=db.session.get(Customer, customer_id)
    if customer:
        return customer_schema.jsonify(customer),200
    else:
         return jsonify({'message':'Customer not found'}),404



@customers_bp.route('/<int:customer_id>', methods=['PUT'])
@customer_token_required    
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    for key, value in customer_data.items():
        setattr(customer, key, value)
    db.session.commit()
    return customer_schema.jsonify(customer), 200

@customers_bp.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404

    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': f'Customer id:{customer_id}, was deleted successfully'}), 200


@customers_bp.route('/<int:customer_id>/service_tickets', methods=['GET'])
@customer_token_required
def get_customer_service_tickets(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404

    tickets = db.session.execute(
        select(ServiceTickets).where(ServiceTickets.customer_id == customer_id)
    ).scalars().all()
    return jsonify(service_tickets_schema.dump(tickets)), 200