#!/bin/sh

sleep 2

celery -A src.celery worker --loglevel=DEBUG
