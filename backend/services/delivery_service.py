from models import db, Order, DeliveryBoy
from kafka_producer import produce_status_update

def accept_order(order_id, delivery_boy_id):
    order = Order.query.get(order_id)
    if order:
        order.delivery_boy_id = delivery_boy_id
        order.status = "Accepted"
        db.session.commit()
        produce_status_update('order_status', {'order_id': order_id, 'status': 'Accepted'})

def update_order_status(order_id, status):
    order = Order.query.get(order_id)
    if order:
        order.status = status
        db.session.commit()
        produce_status_update('order_status', {'order_id': order_id, 'status': status})

def process_order(order_data):
    # Process order received from Kafka and add it to DB
    order = Order(
        customer_id=order_data['customer_id'],
        delivery_location=order_data['delivery_location'],
        status=order_data['status']
    )
    db.session.add(order)
    db.session.commit()

def update_location(delivery_boy_id, current_location):
    delivery_boy = DeliveryBoy.query.get(delivery_boy_id)
    if delivery_boy:
        delivery_boy.current_location = current_location
        db.session.commit()
        produce_status_update('location_updates', {
            'delivery_boy_id': delivery_boy_id,
            'current_location': current_location
        })
