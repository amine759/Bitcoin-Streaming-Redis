# Use an official Python runtime as the base image
FROM python:3.8.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/
COPY .env /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the port that your app runs on
EXPOSE 8050

# Create a startup script that runs the publisher, subscriber, and Dash app
CMD ["bash", "-c", "python3 publisher.py & python3 subscriber.py & python3 dash_app.py"]