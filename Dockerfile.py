# pull the official base image
FROM python:3-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apk update 
RUN apk add musl-dev mariadb-dev gcc
RUN pip install mysqlclient
RUN pip install pymysql

COPY ./requirements.txt /usr/src/app
# Install required library libmysqlclient (and build-essential for building mysqlclient python extension)
#RUN apk add --update python3 python3-dev default-libmysqlclient-dev libmysqlclient
#RUN apk update \
    #&& apk add --virtual build-deps gcc  musl-dev \
 #   && add gcc musl-dev mariadb-connector-c-dev\
  #  && apk add --no-cache mariadb-dev

#RUN pip install mysqlclient  
#RUN pip install default-libmysqlclient-dev  


#RUN apk del build-deps
# RUN apk add  python3-dev libsasl libcrypto1.1 libssl1.1 musl  
#     #&& libldap  \
#     #&&  valgrind
# RUN set -eux && \
#     #export DEBIAN_FRONTEND=noninteractive && \
#     #apk add  build-essential && \
#     apk  update &&\
#     rm -rf /var/lib/apt/lists/*
RUN pip3 install -r requirements.txt

# copy project
COPY . /usr/src/app

EXPOSE 8000
EXPOSE 3306

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]