#!/bin/sh

gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80 --forwarded-allow-ips="*" 