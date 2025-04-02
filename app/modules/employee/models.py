from app.extensions import db
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid

class Employee(db.Model):
    __tablename__ = 'employees'
    __table_args__ = {'schema': 'hr'}
    
    id = db.Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4,
        server_default=db.text("gen_random_uuid()")
    )
    user_id = db.Column(
        UUID(as_uuid=True), 
        db.ForeignKey('auth.users.id'), 
        unique=True,
        nullable=False
    )
    full_name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.Numeric(10, 2))
    department = db.Column(db.String(50))
    metadata_ = db.Column('metadata', JSONB) 
    
    user = db.relationship('User')