from . import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    delivery_boy_id = db.Column(db.Integer, db.ForeignKey('delivery_boy.id'), nullable=True)
    delivery_location = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Order Placed')
