FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir flask gunicorn

# Copy application files
COPY app.py /app/

# Create logs directory
RUN mkdir -p /app/logs

# Expose port
EXPOSE 8888

# Run with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8888", "--access-logfile", "/app/logs/access.log", "--error-logfile", "/app/logs/error.log", "--access-logformat", "%(h)s %(l)s %(u)s %(t)s \"%(r)s\" %(s)s %(b)s \"%(f)s\" \"%(a)s\"", "app:app"]
