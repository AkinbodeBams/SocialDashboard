FROM python:3.9-alpine
LABEL maintener="akinbode"

COPY ./socialmediadashboard/requirements.txt socialmediadashboard/requirements.txt
COPY ./socialmediadashboard /socialmediadashboard
WORKDIR /socialmediadashboard


RUN python -m venv /py && \
    /py/bin/pip install -r requirements.txt && \
    adduser --disabled-password --no-create-home django-user

ENV PATH="/py/bin:$PATH"

USER django-user
