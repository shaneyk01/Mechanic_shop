from app.extensions import ma
from app.models import Mechanic




class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic # type: ignore
        load_only = ("password",)
mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)