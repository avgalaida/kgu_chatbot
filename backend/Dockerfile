FROM python:3.10.0-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /django_app

COPY . /django_app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt