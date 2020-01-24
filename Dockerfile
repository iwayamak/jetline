FROM python:3-slim

RUN mkdir -p /opt/app/jetline
COPY requirements.txt /opt/app/jetline
RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pip3 install --upgrade -r /opt/app/jetline/requirements.txt

RUN mkdir -p /opt/app/jobs
COPY jetline/ /opt/app/jetline

COPY jobs/ /opt/app/jobs
WORKDIR /opt/app/jobs

RUN mkdir -p /tmp/logs

ENV PYTHONPATH /opt/app/:/opt/app/jetline
ENTRYPOINT ["python3", "/opt/app/jetline/kicker.py"]
