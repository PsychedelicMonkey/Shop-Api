FROM python:3.10-alpine

RUN apk update --no-cache && \
    apk add gcc python3-dev libffi-dev

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
