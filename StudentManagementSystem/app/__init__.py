# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:19145569@localhost/confytech'
    app.config['SECRET_KEY'] = '52087318ea97c1280f2fe2bb4d13327ef85802c2f27f1a1d'

    db = SQLAlchemy(app)
    migrate = Migrate(app, db)

    from app import routes  # Import routes at the end to avoid circular imports

    return app
