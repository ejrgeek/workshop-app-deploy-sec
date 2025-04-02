from app import create_app
from app.extensions import db
from app.modules.auth.models import User

app = create_app()

# ESSE ARQUIVO É APENAS DE DEMONSTRAÇÃO, NÃO SE DEVE FAZER ISSO NO MUNDO REAL

with app.app_context():
    admin = User(
        username='admin',
        email='admin@empresa.com',
        is_active=True,
        role='admin'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    print("✅ Admin user created!")