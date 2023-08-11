# pull the official docker image
FROM python:3.11.1-slim

# Set the timezone to Asia/Tashkent
ENV TZ=Asia/Tashkent

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

CMD ["alembic", "upgrade", "head", "&&", "gunicorn", "-b", "0.0.0.0:8000", "main:app", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker"]

