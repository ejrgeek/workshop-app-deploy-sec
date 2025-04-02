from app.extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, ENUM
import uuid

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'auth'}
    
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=db.text("gen_random_uuid()")
    )
    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
        index=True
    )
    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False,
        index=True
    )
    password_hash = db.Column(
        db.String(128),
        nullable=False
    )
    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )
    role = db.Column(
        ENUM('admin', 'manager', 'user', name='user_roles', create_type=False),
        default='user',
        nullable=False
    )
    last_login = db.Column(
        TIMESTAMP(timezone=True),
        server_default=db.func.now()
    )
    created_at = db.Column(
        TIMESTAMP(timezone=True),
        server_default=db.func.now(),
        nullable=False
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=16
        )

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)