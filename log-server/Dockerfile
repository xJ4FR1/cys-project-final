FROM python:3.11-alpine

WORKDIR /app

COPY convert_logs.py .

RUN chmod +x convert_logs.py

EXPOSE 8080

CMD ["python3", "convert_logs.py"]
