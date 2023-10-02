#!/bin/bash

if [[ "${1}" == "celery" ]]; then
  celery --app=app.utils.celery.tasks:send_log_task worker -l INFO
elif [[ "${1}" == "flower" ]]; then
  celery --app=app.utils.celery.tasks:send_log_task flower
fi