FROM python:3.9.2

RUN pip install --upgrade pip

COPY requirements.txt /model/requirements.txt
WORKDIR /model

RUN pip install -r requirements.txt

COPY . /model