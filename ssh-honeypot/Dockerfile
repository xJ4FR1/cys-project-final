FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir paramiko

# Copy application
COPY ssh_honeypot.py /app/
COPY ssh_host_rsa_key /app/

# Create logs directory
RUN mkdir -p /app/logs

# Expose SSH port
EXPOSE 222

# Run the honeypot
CMD ["python", "-u", "ssh_honeypot.py"]
