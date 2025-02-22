# pull the official docker image
FROM python:3.11.1-slim

# Set the timezone to Asia/Tashkent

# set work directory
WORKDIR /code

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy project
COPY . .

ENV TZ=Asia/Tashkent

# RUN apt-get update && \
#     apt-get install -y nginx && \
#     rm -rf /etc/nginx/sites-enabled/default
# COPY nginx.conf /etc/nginx/sites-enabled/

EXPOSE 80

# Запускаем Nginx и Gunicorn для приложения FastAPI
CMD alembic upgrade head && gunicorn -b 0.0.0.0:8000 -w 2 -k uvicorn.workers.UvicornWorker main:app

