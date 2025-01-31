# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variable for Flask
ENV FLASK_APP=app

# Create the database (using module syntax to ensure proper import resolution)
RUN python -m flask db init || true && \
    python -m flask db migrate || true && \
    python -m flask db upgrade || true

# Run initialization script
RUN python create_db.py

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]