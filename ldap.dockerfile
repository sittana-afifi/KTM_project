FROM python:3.9.2 AS ldap-build
RUN pip install --upgrade pip
RUN apt-get update -y && \ 
    pip install --upgrade pip &&\
    pip install --upgrade pip setuptools wheel && \
    apt-get install -y libsasl2-dev libldap2-dev libssl-dev && \
    python -m pip wheel --wheel-dir=/tmp python-ldap


FROM python:3.9.2
COPY --from=ldap-build /tmp/*.whl /tmp/
RUN pip install --upgrade pip
RUN python -m pip install /tmp/*.whl
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
#RUN cd /code/KTM/KTM_Project
# RUN ls -rlt
# RUN cd KTM/KTM_Project
# RUN pwd
# RUN python manage.py makemigrations
# RUN python manage.py migrate
# CMD ["python", "manage.py", "runserver","0.0.0.0:8000"]
EXPOSE 8000
# CMD tail -f /dev/null