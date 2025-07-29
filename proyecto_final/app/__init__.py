from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'clave_secreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foro.db'

    db.init_app(app)

    from .models import User, Question  # importa los modelos
    with app.app_context():
        db.create_all()

    from .routes import main
    app.register_blueprint(main)

    return app

