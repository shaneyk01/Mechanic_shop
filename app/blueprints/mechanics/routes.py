from flask import jsonify, request
from marshmallow import ValidationError 
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from . import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema
from app.models import Mechanic, db, ticket_mechanic


@mechanics_bp.route('/', methods=['POST'])
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    query = select(Mechanic).where(Mechanic.email == mechanic_data['email'])
    existing_mechanic = db.session.execute(query).scalars().first()

    if existing_mechanic:
        return jsonify({'message': 'mechanic with this email already exists.'}), 400

    new_mechanic = Mechanic(**mechanic_data)  
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201


@mechanics_bp.route('/',methods=['GET'])
def get_mechanics():
    query =select(Mechanic)
    mechanics= db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(mechanics), 200

@mechanics_bp.route('/<int:mechanic_id>', methods=['PUT'])
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({'message': 'Mechanic not found'}), 404
    try:
        mechanic_data = mechanic_schema.load(request.json) 
    except ValidationError as e:
        return jsonify(e.messages), 400
    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200

@mechanics_bp.route('/<int:mechanic_id>', methods=['DELETE'])
def delete_mechanic(mechanic_id):
    try:
        mechanic = db.session.get(Mechanic, mechanic_id)
        if not mechanic:
            return jsonify({'message': 'Mechanic not found'}), 404

        # Clear many-to-many associations before deleting
        db.session.execute(
            delete(ticket_mechanic).where(
                ticket_mechanic.c.mechanic_id == mechanic_id
            )
        )

        db.session.delete(mechanic)
        db.session.commit()
        return jsonify({'message': 'Mechanic deleted successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Deletion failed', 'detail': str(e)}), 500