from . import db

class DeliveryBoy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False, unique=True)
    current_location = db.Column(db.String(200), nullable=True)

    orders = db.relationship('Order', backref='delivery_boy', lazy=True)
