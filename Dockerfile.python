# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy over the requirements.txt file
COPY requirements.txt .

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install jupyter_client
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install flake8
# Copy over the rest of the app code
COPY . .

# Set environment variables (if any)
# ENV VARIABLE_NAME=value

# Expose the port the app runs on
EXPOSE 8083

# Start the app
CMD ["python", "app.py"]
