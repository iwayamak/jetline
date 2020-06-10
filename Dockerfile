FROM python:3-slim

# install package
RUN apt-get update && apt-get install -y libpq-dev gcc

# create jetline root dirctory
RUN mkdir -p /opt/app/jetline

# set working directory
COPY jobs/ /opt/app/jetline/jobs
WORKDIR /opt/app/jetline/jobs

# put jetline package
COPY jetline/ /opt/app/jetline/jetline

# pip install required modules
COPY requirements /opt/app/jetline/requirements
COPY requirements.txt /opt/app/jetline
RUN pip3 install --upgrade -r /opt/app/jetline/requirements.txt

# create log directory
RUN mkdir -p /opt/app/jetline/logs

# set python path
ENV PYTHONPATH /opt/app/:/opt/app/jetline

# set entry point
ENTRYPOINT ["python3", "/opt/app/jetline/jetline/kicker.py"]
