# Dockerfile

# Use the official Python image as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Ensure .env.config is copied
COPY .env.config /app/

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
