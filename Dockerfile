FROM python:3.11.6-alpine3.18

COPY requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

COPY . /shared
RUN pip install /shared
