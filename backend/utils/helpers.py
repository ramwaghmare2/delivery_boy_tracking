def validate_delivery_boy_data(data):
    required_fields = ['delivery_boy_id', 'current_location']
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    return True, "Valid data"
