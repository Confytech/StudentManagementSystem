from flask import Flask
from app import app, db  # Import the app and db instance from the app package

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
