from flask import Flask, render_template,request,jsonify
from routes import delivery_routes
from flask_migrate import Migrate
from models import init_db, db, create_tables ,LocationUpdates
from kafka_consumer import consume_orders
import threading
from flask_socketio import SocketIO,emit
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__, template_folder="../frontend", static_folder="../frontend", static_url_path='/static')
CORS(app)
socketio = SocketIO(app)

app.config.from_object('config.Config')

# Initialize DB
init_db(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Register delivery routes
app.register_blueprint(delivery_routes.bp)

# Serve the home page
@app.route('/')
def home():
    return render_template('delivery_home.html')

# Serve the delivery tracking page
@app.route("/delivery_tracking")
def delivery_tracking():
    order_id = request.args.get('orderId')
    delivery_location = request.args.get('delivery_location')
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    print(f"Latitude: {latitude}, Longitude: {longitude}, Delivery location: {delivery_location}")
    return render_template('delivery_tracking.html', order_id=order_id ,
                                                    delivery_location=delivery_location ,
                                                    latitude =latitude,
                                                    longitude=longitude )
@socketio.on('connect')
def handle_connect():
    print("Client connected")
    
# Run the Kafka consumer inside the app context
def start_kafka_consumer():
    with app.app_context():
        consume_orders(socketio)

# Store updates in memory 
location_updates_batch = []

@app.route('/update_delivery_location', methods=['POST'])
def update_delivery_location():
    global location_updates_batch  # Ensure that the global batch list is accessible
    data = request.get_json()
    delivery_boy_id = data.get('delivery_boy_id')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    current_time = datetime.now().strftime('%I:%M:%S %p')

    # Initialize location_updates_batch if it's not already initialized
    if location_updates_batch is None:
        location_updates_batch = []

    # Add the current update to the batch list
    location_updates_batch.append({
        'delivery_boy_id': delivery_boy_id,
        'latitude': latitude,
        'longitude': longitude,
        'created_at': current_time
    })

    # Perform bulk insertion after collecting 20 updates
    if len(location_updates_batch) == 20:
        bulk_insert_location_updates(location_updates_batch)
        location_updates_batch = []  # Reset the batch list after insertion

    # Call Kafka producer to send location update
    from kafka_producer import produce_status_update
    produce_status_update('delivery_location_updates', {
        'delivery_boy_id': delivery_boy_id,
        'latitude': latitude,
        'longitude': longitude
    })

    return jsonify({"status": "success"}), 200

def bulk_insert_location_updates(batch):
    try:
        # Create LocationUpdates objects for bulk insertion
        updates = [
            LocationUpdates(
                delivery_boy_id=item['delivery_boy_id'],
                latitude=item['latitude'],
                longitude=item['longitude'],
                created_at=item['created_at']
            ) for item in batch
        ]

        # Use SQLAlchemy add_all to perform bulk insert
        db.session.add_all(updates)
        db.session.commit()

        # Print a message to the terminal indicating successful insertion
        print(f"Inserted {len(batch)} location updates into the database.")

    except Exception as e:
        # Rollback the session in case of error
        db.session.rollback()
        print(f"Error during bulk insertion: {str(e)}")


if __name__ == "__main__":
    with app.app_context():
        create_tables()
        consumer_thread = threading.Thread(target=start_kafka_consumer)
        consumer_thread.daemon = True 
        consumer_thread.start()
        
    socketio.run(app, debug=True, port=5001)
