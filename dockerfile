FROM ubuntu:latest

LABEL maintainer="Collin Pendleton <collinp@collinpendleton.com>"

ARG DEBIAN_FRONTEND=noninteractive

# Create location where camm info is stored
RUN mkdir /data
# Make sure the package repository is up to date.
RUN apt update && \
    apt -qy upgrade && \
    apt install -qy python3 && \
    apt install -qy git && \
    apt install -qy nmap && \
    apt install -qy software-properties-common && \
    apt install -qy python3-pip && \
    apt install -qy curl && \
    apt install -qy cron && \
    apt install -qy supervisor

RUN git clone https://github.com/madeofpendletonwool/camm.git && \
    cp -R /camm /data && \
    cp /camm/supervisord.conf /etc/supervisord.conf

ENTRYPOINT /bin/bash -c "echo '/usr/bin/python3 /camm/CAMM.py -s $SUBNETS' > /camm/cammtask.sh && crontab -l 2>/dev/null; echo '$RUNTIMER /usr/bin/bash /camm/cammtask.sh' | crontab - && service cron start && tail -f /dev/null"