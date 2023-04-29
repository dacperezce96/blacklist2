from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


db = SQLAlchemy()

class BlackUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    app_uuid = db.Column(db.String(255))
    blocked_reason = db.Column(db.String(255))
    ip = db.Column(db.String(255))
    created_date = db.Column(db.DateTime, default=datetime.now())

class BlackUserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BlackUser
        include_relationships = True
        load_instance = True