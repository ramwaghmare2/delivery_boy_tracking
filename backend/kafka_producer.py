from kafka import KafkaProducer
import json
import requests

def get_kafka_producer():
    return KafkaProducer(
        bootstrap_servers='delivery_boy_kafka:9094',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def produce_status_update(topic, message):
    producer = get_kafka_producer()
    print(f"Producing message to topic '{topic}': {message}")
    producer.send(topic, message)
    producer.flush()

def send_location_update(lat, lng):
    url = 'http://13.232.113.128/update_location'  # Flask backend endpoint
    location_data = {'lat': lat, 'lng': lng}
    
    try:
        response = requests.post(url, json=location_data)
        if response.status_code == 200:
            print("Location sent successfully")
        else:
            print("Failed to send location:", response.status_code, response.text)
    except Exception as e:
        print("Error sending location:", e)

# Example usage (you would call this periodically with the real delivery boy's location)
# send_location_update(19.0760, 72.8777)  # Replace with actual location data
