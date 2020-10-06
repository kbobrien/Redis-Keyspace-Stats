FROM python:3.7.5-slim-buster

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY src/redis_keyspace_stats.py .

CMD ["python", "redis_keyspace_stats.py"]
