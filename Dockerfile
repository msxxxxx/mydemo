#FROM python:3.11.7-alpine3.19
#
#ARG APP_PATH=/opt
#ARG UNAME=www
#ARG UID=1000
#
#WORKDIR $APP_PATH
#
#ENV \
#    PYTHONDONTWRITEBYTECODE=1 \
#    PYTHONUNBUFFERED=1 \
#    PYTHONFAULTHANDLER=1
#
#
#COPY ./demo $APP_PATH/demo
#COPY ./src $APP_PATH/src
#
#RUN apk add build-base && \
#    pip install --no-cache-dir --upgrade -r $APP_PATH/demo/requirements.txt && \
#    adduser -u $UID -s /bin/bash -D -S $UNAME
#USER $UNAME
FROM python:3.11.7-slim

WORKDIR /opt

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

COPY requirements.txt /opt/requirements.txt

RUN pip install --no-cache-dir -r /opt/requirements.txt
