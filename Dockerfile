# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the contents of the employee_management directory into the container at /app
COPY employee_management/ .

# Install Flask and any other necessary dependencies
RUN pip install --no-cache-dir Flask
RUN pip install mysql-connector-python

# Expose the port the application runs on
EXPOSE 5000

# Define environment variable for Flask
ENV FLASK_APP=employee_management_app.py

# Run the command to start the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]
