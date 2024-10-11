from geopy.distance import geodesic

def calculate_distance(location1, location2):
    return geodesic(location1, location2).meters

def get_eta(current_location, destination_location):
    # Just a dummy logic for ETA calculation
    distance = calculate_distance(current_location, destination_location)
    avg_speed = 40  # Assuming 40 km/h speed
    eta = (distance / 1000) / avg_speed * 60  # ETA in minutes
    return round(eta, 2)
