from flask import Blueprint

bp = Blueprint('delivery_routes', __name__)

# Import routes
from . import delivery_routes
