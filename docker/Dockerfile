FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file first to leverage Docker caching
COPY ../backend/requirements.txt /app/requirements.txt

# Install the dependencies from the requirements.txt file
RUN pip install --no-cache-dir --upgrade pip && pip install --timeout=100 -r requirements.txt

# Now copy the rest of the application code
COPY ../backend /app

# Expose the port the Flask app runs on
EXPOSE 5001

# Run the Flask application
CMD ["python", "app.py"]
