FROM nginx

MAINTAINER Swimlane

RUN apt-get clean
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install curl bash iputils-ping
# Cleaning caches
RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false
COPY /nginx.conf /etc/nginx/nginx.conf