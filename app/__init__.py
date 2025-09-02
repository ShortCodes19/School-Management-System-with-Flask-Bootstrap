from .extensions import db, login_manager
from .models import User, Student, Teacher
from flask import Flask
from flask_migrate import Migrate

def create_app(config_object='config.Config'):
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(config_object)

    db.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)

    from .auth import auth_bp
    from .views import views_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(views_bp)

    return app