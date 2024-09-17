FROM python:3.12-slim as build

ARG FLASK_APP
ARG FLASK_DEBUG
ARG FLASK_ENV
ARG SECRET_KEY
ARG PORT

ENV FLASK_APP=${FLASK_APP} \
    FLASK_DEBUG=${FLASK_DEBUG} \
    FLASK_ENV=${FLASK_ENV} \
    SECRET_KEY=${SECRET_KEY} \
    PORT=${PORT} \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /opt/jounce

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements/ /opt/jounce/requirements/

RUN pip install --no-cache-dir -r /opt/jounce/requirements/dev.txt

COPY . .

FROM python:3.12-slim

ENV FLASK_APP=${FLASK_APP} \
    FLASK_DEBUG=${FLASK_DEBUG} \
    FLASK_ENV=${FLASK_ENV} \
    SECRET_KEY=${SECRET_KEY} \
    PORT=${PORT} \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /opt/jounce

COPY --from=build /usr/local /usr/local
COPY --from=build /opt/jounce /opt/jounce

RUN chmod +x /opt/jounce/entrypoint.sh
RUN chmod +x /opt/jounce/startworker.sh

RUN echo "PATH: $PATH"
