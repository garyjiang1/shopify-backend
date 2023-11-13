# pull official base image
FROM python:3.8.0-alpine
# set work directory
WORKDIR /usr/src/app

RUN apk update && apk add bash
# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
# copy project
COPY ../Downloads/Shopify-Backend-Project-main /usr/src/app/


CMD ["/bin/sh", "/usr/src/app/docker-entrypoint.sh"]




