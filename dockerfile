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
# Install a basic SSH server
#     apt install -qy openssh-server && \
#     sed -i 's|session    required     pam_loginuid.so|session    optional     pam_loginuid.so|g' /etc/pam.d/sshd && \
#     mkdir -p /var/run/sshd
# # Generate ssh key in root
# RUN ssh-keygen -q -t rsa -N '' -f /id_rsa
# Create new camm user
# RUN adduser --gecos "" --disabled-password --quiet camm && \
#         echo "camm:camm" | chpasswd && \
#     mkdir /home/camm/.m2 && \
#         mkdir /home/camm/.ssh
# RUN chown -R camm:camm /id_rsa.pub && \
#     chown -R camm:camm /id_rsa && \
#     chmod 0755 /id_rsa && \
#     chown 0755 /id_rsa.pub && \
#     chown -R camm:camm /home/camm/.m2/ && \
#     chown -R camm:camm /home/camm/.ssh/
# Put camm Files in place
RUN git clone https://github.com/madeofpendletonwool/camm.git && \
    cp -R camm /data && \
    cp /camm/setup.sh / &&\
    chmod 777 /setup.sh
COPY /camm/supervisord.conf /etc/supervisord.conf
# Begin CAM Setup
# RUN (crontab -l 2>/dev/null; echo "@reboot /data/camm/setup.sh $RUNTIMER $SUBNETS") | crontab -
#     # crontab -l > cammbootcron && \
#     #echo new cron into cron file
#     # echo "@reboot /data/setup.sh $RUNTIMER $SUBNETS" >> cammbootcron && \
#     #install new cron file
#     # crontab cammbootcron
# ENTRYPOINT /bin/bash -c "echo test"
ENTRYPOINT /bin/bash -c "(crontab -l 2>/dev/null; echo '$RUNTIMER /usr/bin/python3 /data/CAMM.py $SUBNETS') | crontab -" && supervisord /etc/supervisord.conf
CMD tail -f /dev/null