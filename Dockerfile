FROM ubuntu:latest
WORKDIR /app
RUN apt-get update 
RUN apt-get install -y python3-pip python3 libsasl2-dev python3-dev libldap2-dev libssl-dev python3-ldap libmysqlclient-dev  mysql-client && pip3 install python-ldap --user
COPY . /app
RUN pip3 install -r /app/requirements.txt 	
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/py/bin:$PATH"
EXPOSE 8000











# # syntax=docker/dockerfile:1
# # FROM ldap_build:latest
# #FROM python:3.9.2
# FROM ubuntu:20.04
# #ARG DEBIAN_FRONTEND=interactive
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
# WORKDIR /code
# #COPY requirements.txt /code
# # RUN apt-get update -y && \
# #     apt-get install -y python3-pip
# RUN apt-get update
# RUN apt-get install -y python3 python python3-pip libsasl2-dev libldap2-dev libssl-dev 
# COPY . /code
# RUN  pip3 install -r requirements.txt requirements.txt
# ENV PATH="/py/bin:$PATH"
# #RUN cd /code/KTM/KTM_Project
# # RUN ls -rlt
# # RUN cd KTM/KTM_Project
# # RUN pwd
# # RUN python manage.py makemigrations
# # RUN python manage.py migrate
# #CMD ["python", "manage.py", "runserver","0.0.0.0:8000"]
# EXPOSE 8000
#pull the official base image
# FROM python:3

