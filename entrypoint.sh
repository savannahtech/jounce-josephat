#!/bin/bash

flask db upgrade \
&& python manage.py initialize_metrics \
&& python manage.py initialize_llms 

if [ "$RUN_SERVER" = "true" ]; then
    gunicorn --bind :5000 app:app --log-level DEBUG --timeout 90 --workers 3
fi
