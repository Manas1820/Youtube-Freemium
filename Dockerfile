FROM python:3.9-slim

# Create a group and user to run our app
ENV APP_USER=user
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}

# Install packages needed to run your application (not build deps):
#   mime-support -- for mime types when serving static files
#   postgresql-client -- for running database commands
# We need to recreate the /usr/share/man/man{1..8} directories first because
# they were clobbered by a parent image.

RUN set -ex \
    && RUN_DEPS=" \
    libpcre3 \
    mime-support \
    postgresql-client \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && rm -rf /var/lib/apt/lists/*

# Determine if we are going to use the dev or prod stuff
ENV RUNTIME=Prod
# Copy in your pord requirements file
ADD requirements.txt /requirements.txt

# Install build deps, then run `pip install`, then remove unneeded build deps
# all in a single step.
# Correct the path to your production requirements file, if needed.
RUN set -ex \
    && BUILD_DEPS=" \
    build-essential \
    libpcre3-dev \
    libpq-dev \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r /requirements.txt \
    \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/*

# Copy your application code to the container (make sure you create a .dockerignore 
# file if any large files or directories should be excluded)
RUN mkdir /backend/
WORKDIR /backend/
ADD . /backend/
RUN chmod -R a+rwx /backend/
# RUN chown ${APP_USER}:${APP_USER} /backend/

# Set up required env variables for managepy to run
ENV DJANGO_SETTINGS_MODULE="backend.config"
ENV DJANGO_CONFIGURATION=${RUNTIME}

# Change to a non-root user
# Comment or uncomment if it is available
# USER ${APP_USER}:${APP_USER}

EXPOSE 8000

# Run the celery worker
# Change it to any other command based on your file
CMD ["start"]