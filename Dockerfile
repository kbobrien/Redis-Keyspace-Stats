FROM python:3.7.5-slim-buster
RUN python -m pip install \
        redis

COPY src/redis_keyspace_stats.py .

CMD ["python", "redis_keyspace_stats.py"]
