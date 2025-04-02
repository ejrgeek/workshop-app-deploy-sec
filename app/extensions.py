from flask import redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_talisman import Talisman

db = SQLAlchemy(engine_options={
    'pool_pre_ping': True,
    'pool_size': 10,
    'max_overflow': 30,
    'pool_recycle': 3600
})

login_manager = LoginManager()
migrate = Migrate()
talisman = Talisman()

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))