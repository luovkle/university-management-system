FROM python:3.10.9-alpine3.17
WORKDIR /app
COPY ["app/requirements.txt", "/app/"]
RUN pip install -r requirements.txt
COPY ["app/pictures", "/app/pictures/"]
COPY ["app/alembic.ini", "/app/"]
COPY ["app/alembic", "/app/alembic/"]
COPY ["app/app", "/app/app/"]
