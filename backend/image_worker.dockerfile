FROM python:3.10.8-bullseye
WORKDIR /app
COPY ["app/requirements.txt", "/app/"]
RUN pip install -r requirements.txt
COPY ["./image_worker/app", "/app/app/"]
COPY ["./image_worker/files", "/app/files"]
