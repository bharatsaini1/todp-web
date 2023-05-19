from app import db, app, TODO

with app.app_context():
    db.create_all()
