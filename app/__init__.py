from flask import Flask, abort, redirect, url_for
from jinja2 import ChoiceLoader, FileSystemLoader, PrefixLoader
from .config import Config
from .extensions import db, login_manager, migrate


def create_app():
    app = Flask(__name__, static_folder='static')

    if not app.debug:
        import logging
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)

    app.jinja_loader = ChoiceLoader([
        app.jinja_loader,
        PrefixLoader({
            'auth': FileSystemLoader('app/modules/auth/templates/auth'),
            'employee': FileSystemLoader('app/modules/employee/templates/employee')
        })
    ])

    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    migrate.init_app(app, db)
    
    from .modules.auth.routes import auth_bp
    from .modules.employee.routes import employee_bp
    from app.errors.handlers import bp as errors_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(errors_bp)
    
    @app.template_filter('format_date')
    def format_date(value, format='%d/%m/%Y'):
        if value is None:
            return ''
        return value.strftime(format)
    
    @app.template_filter('format_currency')
    def format_currency(value):
        if value is None:
            return ''
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    @app.route('/')
    def redirect_to_employee_list():
        return redirect(url_for('employee.list_employees'))
    
    @app.route('/login')
    def redirect_to_auth_login():
        return redirect(url_for('auth.login'))

    @app.route('/register')
    def redirect_to_auth_register():
        return redirect(url_for('auth.register'))
    
    @app.route('/test/400')
    def test_400():
        abort(400)

    @app.route('/test/401')
    def test_401():
        abort(401)

    @app.route('/test/403')
    def test_403():
        abort(403)

    @app.route('/test/404')
    def test_404():
        abort(404)

    @app.route('/test/500')
    def test_500():
        abort(500)
    
    return app