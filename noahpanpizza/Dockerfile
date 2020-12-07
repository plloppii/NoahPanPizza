# pull official base image
FROM python:3.8.3-alpine

# set work directory
WORKDIR /usr/src/noahpanpizza

# set environment variables
#prevent python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE 1 
#prevent python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

RUN apk add --update --no-cache --virtual .tmp gcc libc-dev \
    openssl-dev python3-dev musl-dev 

RUN apk add jpeg-dev zlib-dev \
    libxml2 libxslt-dev libffi-dev \
    postgresql-dev 

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
# remove virtual packages that are only needed for pip
RUN apk del .tmp

COPY ./entrypoint.sh .

# copy project
COPY . .

ENTRYPOINT [ "/usr/src/noahpanpizza/entrypoint.sh" ]