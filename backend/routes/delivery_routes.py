from flask import Blueprint, request, jsonify, render_template
from services.delivery_service import accept_order, update_order_status, update_location
from kafka import KafkaConsumer, KafkaProducer, errors
import json
import time
from models import DeliveryBoy

bp = Blueprint('delivery_routes', __name__)

# Function to create a Kafka consumer with retry logic
def get_kafka_consumer():
    consumer = None
    for attempt in range(5):  # Retry up to 5 times
        try:
            consumer = KafkaConsumer(
                'order_topic',
                bootstrap_servers='kafka:9092',
                value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                auto_offset_reset='earliest'
            )
            break  # Exit the loop if consumer is successfully created
        except errors.NoBrokersAvailable:
            print(f"Attempt {attempt+1}: Kafka broker not available, retrying in 5 seconds...")
            time.sleep(5)
    
    if consumer is None:
        raise Exception("Failed to connect to Kafka broker after 5 retries")
    
    return consumer

# Function to create a Kafka producer with retry logic
def get_kafka_producer():
    producer = None
    for attempt in range(5):  # Retry up to 5 times
        try:
            producer = KafkaProducer(
                bootstrap_servers='kafka:9092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            break  # Exit the loop if producer is successfully created
        except errors.NoBrokersAvailable:
            print(f"Attempt {attempt+1}: Kafka broker not available, retrying in 5 seconds...")
            time.sleep(5)
    
    if producer is None:
        raise Exception("Failed to connect to Kafka broker after 5 retries")
    
    return producer

# Kafka consumer setup to consume orders from Kafka
consumer = get_kafka_consumer()

@bp.route("/get_orders", methods=["GET"])
def get_orders_route():
    orders = []
    try:
        consumer = get_kafka_consumer()  # Get Kafka consumer within the route
        # Consume messages from Kafka
        for message in consumer:
            order = message.value
            orders.append(order)
            if len(orders) >= 10:
                break
        return jsonify({'orders': orders}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route("/accept_order", methods=["POST"])
def accept_order_route():
    try:
        data = request.json
        order_id = data.get('order_id')
        delivery_boy_id = data.get('delivery_boy_id')
        delivery_boy_location = data.get('delivery_boy_location') 

        # Extract latitude and longitude from delivery_boy_location
        latitude = delivery_boy_location.get('latitude') if delivery_boy_location else None
        longitude = delivery_boy_location.get('longitude') if delivery_boy_location else None

        # Call service to update order status in the database
        accept_order(order_id, delivery_boy_id)

        # Create a new Kafka producer instance
        producer = get_kafka_producer()

        # Send acknowledgment back to Kafka
        producer.send('order_status', {
            'order_id': order_id,
            'status': 'Accepted',
            'delivery_boy_id': delivery_boy_id,
            'latitude': latitude,
            'longitude': longitude
        })
        producer.flush()

        return jsonify({'message': 'Order accepted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route("/reject_order", methods=["POST"])
def reject_order_route():
    try:
        data = request.json
        order_id = data.get('order_id')
        delivery_boy_id = data.get('delivery_boy_id')

        # Create a new Kafka producer instance
        producer = get_kafka_producer()

        # Send acknowledgment back to Kafka
        producer.send('order_status', {
            'order_id': order_id,
            'status': 'Rejected',
            'delivery_boy_id': delivery_boy_id
        })
        producer.flush()

        return jsonify({'message': 'Order rejected successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#@bp.route("/accept_order", methods=["POST"])
#def accept_order_route():
   #    return render_template('delivery_tracking.html')

@bp.route("/update_status", methods=["POST"])
def update_status_route():
    try:
        data = request.json
        order_id = data.get('order_id')
        status = data.get('status')

        # Call service to update status in the database
        update_order_status(order_id, status)

        # Create a new Kafka producer instance
        producer = get_kafka_producer()

        # Send status update to Kafka
        producer.send('order_status', {'order_id': order_id, 'status': status})
        producer.flush()

        return jsonify({'message': 'Status updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route("/update_location", methods=["POST"])
def update_location_route():
    try:
        data = request.json
        delivery_boy_id = data.get('delivery_boy_id')
        current_location = data.get('current_location')

        # Update the location of the delivery boy in the database
        update_location(delivery_boy_id, current_location)

        return jsonify({'message': 'Location updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route("/get_delivery_boy_location", methods=["GET"])
def get_delivery_boy_location():
    try:
        delivery_boy_id = request.args.get('delivery_boy_id')
        
        # Assuming you have a DeliveryBoy model with latitude and longitude fields
        delivery_boy = DeliveryBoy.query.get(delivery_boy_id)
        
        if delivery_boy:
            location = {
                "latitude": delivery_boy.current_latitude,
                "longitude": delivery_boy.current_longitude
            }
            return jsonify({"location": location})
        
        return jsonify({"error": "Delivery boy not found"}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
