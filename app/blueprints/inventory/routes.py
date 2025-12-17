from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select

from . import inventory_bp
from .schemas import inventory_schema
from app.models import Inventory, db


@inventory_bp.route('/', methods=['POST'])
def create_inventory_item():
	try:
		inventory_data = inventory_schema.load(request.json)
	except ValidationError as e:
		return jsonify(e.messages), 400

	new_item = Inventory(**inventory_data)
	db.session.add(new_item)
	db.session.commit()
	return inventory_schema.jsonify(new_item), 201


@inventory_bp.route('/', methods=['GET'])
def get_all_item():
	items = db.session.execute(select(Inventory)).scalars().all()
	return inventory_schema.jsonify(items, many=True), 200


@inventory_bp.route('/<int:inventory_id>', methods=['PUT'])
def update_inventory_item(inventory_id):
	item = db.session.get(Inventory, inventory_id)
	if not item:
		return jsonify({'message': 'Inventory item not found'}), 404

	try:
		inventory_data = inventory_schema.load(request.json)
	except ValidationError as e:
		return jsonify(e.messages), 400

	for key, value in inventory_data.items():
		setattr(item, key, value)

	db.session.commit()
	return inventory_schema.jsonify(item), 200


@inventory_bp.route('/<int:inventory_id>', methods=['DELETE'])
def delete_inventory_item(inventory_id):
	item = db.session.get(Inventory, inventory_id)
	if not item:
		return jsonify({'message': 'Inventory item not found'}), 404

	db.session.delete(item)
	db.session.commit()
	return jsonify({'message': f'Inventory item id:{inventory_id} was deleted successfully'}), 200

