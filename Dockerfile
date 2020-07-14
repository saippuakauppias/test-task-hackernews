FROM python:3.7-alpine

WORKDIR /app

RUN apk update
RUN apk add --no-cache postgresql-libs
RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

# https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app
RUN pip install -e .

RUN /usr/bin/crontab /app/crontab.tasks

CMD ["/bin/sh", "/app/entrypoint.sh"]
