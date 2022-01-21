# base image
FROM python:3.8-slim-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_CACHE_DIR='/var/cache/pypoetry'
ENV PATH="$PATH:/root/.poetry/bin"

# install dependencies
RUN apt-get clean
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install netcat curl bash git iputils-ping
RUN apt-get -y install libffi-dev libgtk2.0-dev libgl1-mesa-glx
# Cleaning caches
RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false


# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip3 install "poetry==1.1.6"
COPY poetry.lock pyproject.toml /usr/src/app/

# update pip
RUN /usr/local/bin/python -m pip install --upgrade pip

# Install project requirements
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-dev --no-interaction --no-ansi
RUN pip3 install appdirs

# add app
ADD . /usr/src/app