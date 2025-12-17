from flask import jsonify, request
from marshmallow import ValidationError  # type: ignore
from sqlalchemy import select
from . import service_tickets_bp
from .schemas import service_ticket_schema, service_tickets_schema
from app.blueprints.mechanics.schemas import mechanic_schema
from app.models import ServiceTickets, Mechanic, db

@service_tickets_bp.route('/', methods=['POST'])
def create_service_ticket():
    try:
        ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_ticket = ServiceTickets(**ticket_data)
    db.session.add(new_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_ticket), 201

@service_tickets_bp.route('/', methods=['GET'])
def get_service_tickets():
    tickets = db.session.execute(select(ServiceTickets)).scalars().all()
    return jsonify(service_tickets_schema.dump(tickets)), 200

@service_tickets_bp.route('/<int:service_ticket_id>/add_mechanic/<int:mechanic_id>', methods=['PUT'])
def add_mechanic(service_ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTickets, service_ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not ticket or not mechanic:
        return jsonify({"error": "Invalid mechanic_id or service_ticket_id"}), 400

    if mechanic in ticket.mechanics:
        return jsonify({"error": "Mechanic already assigned"}), 400

    ticket.mechanics.append(mechanic)
    db.session.commit()
    return jsonify({
        "message": "Mechanic added",
        "serviceTicket": service_ticket_schema.dump(ticket),
        "mechanic": mechanic_schema.dump(mechanic),
    }), 200

@service_tickets_bp.route('/<int:service_ticket_id>/remove_mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(service_ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTickets, service_ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not ticket or not mechanic:
        return jsonify({"error": "Invalid mechanic_id or service_ticket_id"}), 400

    if mechanic not in ticket.mechanics:
        return jsonify({"error": "Mechanic not assigned"}), 400

    ticket.mechanics.remove(mechanic)
    db.session.commit()
    return jsonify({
        "message": "Mechanic removed",
        "serviceTicket": service_ticket_schema.dump(ticket),
        "mechanic": mechanic_schema.dump(mechanic),
    }), 200