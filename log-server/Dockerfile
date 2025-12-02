FROM python:3.11-alpine

WORKDIR /app

COPY convert_logs.py .
COPY parse_dionaea.py .

RUN chmod +x convert_logs.py parse_dionaea.py

EXPOSE 8080

CMD ["python3", "convert_logs.py"]
