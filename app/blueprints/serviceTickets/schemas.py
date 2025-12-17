from marshmallow import fields, validate
from app.extensions import ma
from app.models import ServiceTickets
from app.blueprints.mechanics.schemas import MechanicSchema  
class ServiceTicketsSchema(ma.SQLAlchemyAutoSchema):
    # explicit fields
    id = ma.auto_field(dump_only=True)
    date = fields.Date(required=True)
    customer_id = ma.auto_field(required=True)
    service_descr = fields.String(required=True, validate=validate.Length(min=1, max=255))

    # include assigned mechanics in responses (optional)
    mechanics = fields.List(
        fields.Nested(MechanicSchema(only=("id", "name", "email"))),
        dump_only=True
    )

    class Meta:
        model = ServiceTickets
        load_instance = False
        include_fk = True
        include_relationships = True
        # limit output fields (adjust as needed)
        fields = ("id", "date", "customer_id", "service_descr", "mechanics")

service_ticket_schema = ServiceTicketsSchema()
service_tickets_schema = ServiceTicketsSchema(many=True)