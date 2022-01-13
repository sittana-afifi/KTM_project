FROM ubuntu:latest
WORKDIR /app
RUN apt-get update 
RUN apt-get install -y python3-pip python3 libsasl2-dev python3-dev libldap2-dev libssl-dev python3-ldap libmysqlclient-dev  mysql-client && pip3 install python-ldap --user
COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt 	
COPY  . /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
EXPOSE 8000