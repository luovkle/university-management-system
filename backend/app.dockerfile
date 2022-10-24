FROM python:3.10.8-bullseye
WORKDIR /app
COPY ["app/requirements.txt", "/app/"]
RUN pip install -r requirements.txt
COPY ["app/alembic.ini", "/app/"]
COPY ["app/alembic", "/app/alembic/"]
COPY ["app/app", "/app/app/"]
