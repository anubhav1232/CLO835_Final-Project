# Use the official Ubuntu 20.04 base image
FROM ubuntu:20.04

# Set environment variable to avoid interactive prompts during package installations
ENV DEBIAN_FRONTEND=noninteractive

# Update apt package list and install system dependencies
RUN apt-get update -y \
    && apt-get install -y \
    python3-pip \
    mysql-client \
    && apt-get clean

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory content into the container's /app directory
COPY . /app

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install required Python dependencies
RUN pip install -r requirements.txt

# Expose port 8080 for the Flask app to be accessible
EXPOSE 8080

# Set the default command to run the Flask app using python3
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]
