FROM python:3-slim

# create jetline root dirctory
RUN mkdir -p /opt/app/jetline

# pip install required modules
COPY requirements.txt /opt/app/jetline
RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pip3 install --upgrade -r /opt/app/jetline/requirements.txt

# put jetline package
RUN mkdir -p /opt/app/jobs
COPY jetline/ /opt/app/jetline

# get job definition file
COPY jobs/ /opt/app/jobs
WORKDIR /opt/app/jobs

# create log directory
RUN mkdir -p /tmp/logs

# set python path
ENV PYTHONPATH /opt/app/:/opt/app/jetline

# set entry point
ENTRYPOINT ["python3", "/opt/app/jetline/kicker.py"]
