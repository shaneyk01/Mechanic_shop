from app.extensions import ma
from app.models import Customer
from marshmallow import fields



class CustomerSchema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = Customer
            
class CustomerLoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
            
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
login_schema = CustomerLoginSchema()