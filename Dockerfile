FROM python:3-slim

# create jetline root dirctory
RUN mkdir -p /opt/app/jetline

# pip install required modules
COPY requirements.txt /opt/app/jetline
RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pip3 install --upgrade -r /opt/app/jetline/requirements.txt
RUN pip3 install awscli

# put jetline package
RUN mkdir -p /opt/app/jobs
COPY jetline/ /opt/app/jetline

# put kicker_for_docker.sh
COPY kicker_for_docker.sh /opt/app/jetline

WORKDIR /opt/app/jobs
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION
ARG http_proxy
ARG https_proxy
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ENV AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION
ENV http_proxy=$http_proxy
ENV https_proxy=$https_proxy

# create log directory
RUN mkdir -p /tmp/logs


# set python path
ENV PYTHONPATH /opt/app/:/opt/app/jetline

# set entry point
ENTRYPOINT ["/bin/bash", "/opt/app/jetline/kicker.sh"]
