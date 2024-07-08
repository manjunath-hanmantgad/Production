from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from .models import User


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('POSTGRES_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app
