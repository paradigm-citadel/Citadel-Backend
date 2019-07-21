FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN mkdir /config /src /scripts
ADD /config/ /config
ADD /commands/ /commands

RUN pip install -r /config/requirements.txt
WORKDIR /src