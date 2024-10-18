# Customer Order Tracking & Delivery Boy Tracking System

## Overview

This system consists of two main components: 
1. **Customer Order Tracking**: Allows customers to place orders, track order statuses, and view real-time locations of the delivery person.
2. **Delivery Boy Tracking**: Enables delivery boys to accept or reject orders, view customer details, and provide real-time updates on their location during delivery.

Both components communicate with each other using Kafka to exchange real-time order and delivery status updates. The system is built with Flask, Kafka, MySQL, and Docker, and is deployed on AWS EC2.

## Features

### Customer Order Tracking
- Customers can place orders.
- Orders are assigned a status (pending, accepted, delivered).
- Customers can view real-time updates on their order status.
- Real-time tracking of the delivery boy on a map once the order is accepted.

### Delivery Boy Tracking
- Delivery boys can accept or reject orders assigned to them.
- View customer details (name, address, coordinates) after accepting an order.
- Update order status as they proceed with delivery.
- Real-time location updates for customers.

### Communication via Kafka
- **Order Messages**: The customer sends order details to the Kafka topic (`order_topic`).
- **Delivery Updates**: Delivery boys consume order details from Kafka, update status, and send real-time location data to Kafka, which is consumed by the customer interface.

## Technologies Used

- **Backend**: Python, Flask, Flask-SocketIO, Kafka
- **Frontend**: HTML, CSS, JavaScript (Leaflet.js for map, Bootstrap for styling)
- **Database**: MySQL (via SQLAlchemy)
- **Messaging Queue**: Apache Kafka (producer and consumer setup for customer and delivery boy)
- **Real-time Map**: Leaflet.js for displaying real-time location on the map.

## Project Structure

### 1. Customer Order Tracking
![image](https://github.com/user-attachments/assets/a2dc1b01-6b35-43d1-ad67-c8eece314ac4)


```

### 2. Delivery Boy Tracking

```
![image](https://github.com/user-attachments/assets/24cd44f2-cf19-486f-96dc-75e3dcafdb02)

```

---

## Features

### Customer Order Tracking:
- Customers can place orders by filling out a form.
- Track the status of their order in real-time.
- View delivery boy's location using a map.
  
### Delivery Boy Tracking:
- Delivery boys can view available orders and accept/reject them.
- Upon accepting an order, they receive customer details (customer name, location, etc.).
- Provide real-time location updates to customers during the delivery process.

### Real-Time Communication:
- Kafka is used to communicate between the customer and delivery boy services. Orders are produced by the customer system and consumed by the delivery boy system.
  
---

## Kafka Integration

- **Topics**: 
  - `order_topic`: Handles order placement and order status updates.
  - `delivery_topic`: Handles delivery boy's real-time location updates.

Kafka consumers and producers are integrated within the system to ensure real-time updates for both customers and delivery boys.

---

## Docker Setup

Both systems are containerized using Docker. To spin up the environment:

1. **Build the images**:
   ```
   docker-compose build
   ```

2. **Start the services**:
   ```
   docker-compose up
   ```

This will start:
- Flask applications for both customer and delivery boy systems.
- Kafka and Zookeeper services for message communication.
- MySQL databases for storing customer and order information.

---

## AWS EC2 Deployment

The application is deployed on AWS EC2 using Docker Compose. Each EC2 instance hosts:
- Kafka and Zookeeper
- The Flask applications for both customer and delivery boy services
- MySQL databases

### Steps for Deployment:
1. Set up EC2 instances with Docker and Docker Compose.
2. Upload the Docker Compose files and project folders to the EC2 instance.
3. Run the application using `docker-compose up` on each instance.

---

## Requirements

- Python 3.x
- Flask
- Kafka
- MySQL
- Docker & Docker Compose
- Leaflet.js for real-time maps (customer front end)

## Setup Instructions

### 1. Prerequisites
- Python 3.x
- Apache Kafka
- Zookeeper
- MySQL
- Node.js (optional for certain frontend dependencies)

### 2. Clone the Repository

```bash
git clone https://github.com/your_username/customer_delivery_tracking.git
cd customer_order_tracking
```

### 3. Install Dependencies

For both the customer and delivery boy projects, install the required Python packages:

```bash
pip install -r backend/requirements.txt
```

### 4. Configure MySQL

Create the required MySQL databases and tables for both customer and delivery boy models. Set your database connection in `config.py`.

### 5. Start Kafka & Zookeeper

Run Zookeeper and Kafka locally:

```bash
# Start Zookeeper
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties

# Start Kafka
.\bin\windows\kafka-server-start.bat .\config\server.properties
```

### 6. Start the Backend Services

Start both the customer and delivery boy Flask apps:

```bash
# In customer_order_tracking/backend
python app.py

# In delivery_boy_tracking/backend
python app.py
```

### 7. Run Kafka Consumer and Producer

Ensure that your Kafka producer (for the customer) and Kafka consumer (for the delivery boy) are running and listening on the appropriate topics (`order_topic` for orders).

### 8. Open the Frontend

You can access the frontend by opening the `index.html` files for both customers and delivery boys.

- **Customer**: Place orders and track status at `customer_order_tracking/frontend/index.html`.
- **Delivery Boy**: Accept/reject orders and track deliveries at `delivery_boy_tracking/frontend/delivery_home.html`.

### 9. Real-Time Updates

- When a customer places an order, the delivery boy receives customer details in real-time.
- Once the delivery boy accepts the order, the customer can track the delivery boy's location.

   ```



