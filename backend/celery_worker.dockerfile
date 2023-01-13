FROM python:3.10.8-bullseye
WORKDIR /app
COPY ["app/requirements.txt", "/app/"]
RUN pip install $(cat requirements.txt | grep -E "celery|redis|pillow|fastapi")
COPY ["./image_worker/app", "/app/app/"]
CMD ["celery", "-A", "app.celery_worker.celery_app", "worker", "--loglevel=info"]
