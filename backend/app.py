from flask import Flask, render_template,request
from routes import delivery_routes
from flask_migrate import Migrate
from models import init_db, db, create_tables
from kafka_consumer import consume_orders
import threading
from flask_socketio import SocketIO,emit
from flask_cors import CORS


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

if __name__ == "__main__":
    with app.app_context():
        create_tables()
        consumer_thread = threading.Thread(target=start_kafka_consumer)
        consumer_thread.daemon = True 
        consumer_thread.start()
        
    socketio.run(app, debug=True, port=5001)
