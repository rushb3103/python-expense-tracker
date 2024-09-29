# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies directly without virtualenv for simplicity
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Install wget for Ngrok installation
RUN apt-get update && apt -y upgrade

# Expose the ports (Gunicorn on 8000, Ngrok's web interface on 4040)
EXPOSE 8000

# Set the entry point to run Gunicorn and Ngrok
#CMD gunicorn myapp:app --bind 0.0.0.0:8000 & ngrok http 8000
#CMD gunicorn --workers 3 --timeout 120 app:app --bind 0.0.0.0:8000
# Set the entry point to run Gunicorn and Ngrok
CMD gunicorn --workers 3 --timeout 120 app:app --bind 0.0.0.0:8000
