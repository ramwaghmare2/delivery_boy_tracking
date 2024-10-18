from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .order import Order
from .delivery_boy import DeliveryBoy,LocationUpdates

def init_db(app):
    db.init_app(app)

def create_tables():
    with db.engine.connect() as connection:
        db.create_all()
