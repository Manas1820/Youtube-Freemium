#!/bin/bash

set -e

function help_text() {
  cat << 'END'                                                              
Docker entrypoint script for API.
Usage:
  help - print this help text and exit
  server - start the server
  celery - start celery
  (anything else) - run the command provided
END
}


function header() {
  size=${COLUMNS:-80}
  # Print centered text between two dividers of length $size
  printf '#%.0s' $(seq 1 $size) && echo
  printf "%*s\n" $(( (${#1} + size) / 2)) "$1"
  printf '#%.0s' $(seq 1 $size) && echo
}

if [ "$1" == help ] || [ "$1" == --help ]; then help_text && exit 0; fi
sleep 0.1;  # The $COLUMNS variable takes a moment to populate


case "$1" in
  server|"")
    # Start scheduler and webserver in same container
    header "RUNNING MIGRATIONS AND STARTING WSGI SERVER"
    python manage.py collectstatic
    python manage.py migrate
    gunicorn --bind :8000 --workers 3 backend.wsgi
    ;;
  celery)
    celery -A backend worker --beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
    ;;
  *)
    # The command is something like bash. Just run it in the right environment.
    header "RUNNING \"$*\""
    exec "$@"
    ;;
esac