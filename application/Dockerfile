# Use the official Ubuntu 20.04 base image
FROM ubuntu:20.04

# Set environment variable to avoid interactive prompts during package installations
ENV DEBIAN_FRONTEND=noninteractive

# Update apt package list and install system dependencies
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
    python3-pip \
    python3-dev \
    mysql-client \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy only the necessary files first for dependency installation
COPY requirements.txt /app/

# Upgrade pip to the latest version
RUN pip install --no-cache-dir --upgrade pip

# Install required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Expose port 81 for the Flask app to be accessible
EXPOSE 81

# Set the default command to run the Flask app using python3
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]
