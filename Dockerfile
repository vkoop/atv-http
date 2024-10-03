FROM python:3.12-bookworm

# Install dependencies in a single RUN command to reduce layers
RUN apt-get update && \
     apt-get install -y --no-install-recommends build-essential libssl-dev libffi-dev && \
     apt-get clean && \
     rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt && \
     rm /tmp/requirements.txt

# Copy application code
COPY . /app
WORKDIR /app

# Expose the application port
EXPOSE 8080

# Set the default command to run the application
CMD ["python", "-u", "./main.py"]