from kafka import KafkaConsumer
import json
from services.delivery_service import process_order
import time
from flask_socketio import SocketIO,emit



def get_kafka_consumer():
    return KafkaConsumer(
        'order_topic',
        bootstrap_servers='localhost:9092',
        group_id='delivery_boy_group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest'  # Start from earliest if no offset is found
    )

def consume_orders(socketio):
    # Create Kafka consumer for the 'order_topic'
    consumer = get_kafka_consumer()
    
    try:
        # This will block and continuously fetch messages
        for message in consumer:
            print(f"Consumed message: {message.value}")
            # Process the order using your service
            #process_order(message.value)
            socketio.emit('new_order', message.value)
    except Exception as e:
        print(f"Error consuming Kafka message: {e}")
    finally:
        consumer.close()