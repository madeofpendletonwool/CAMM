FROM ubuntu:latest

LABEL maintainer="Collin Pendleton <collinp@collinpendleton.com>"
# Create location where CAMM info is stored
RUN mkdir /data
# Make sure the package repository is up to date.
RUN apt update && \
    apt -qy upgrade && \
    apt install -qy python3 \
    apt install -qy git && \
    apt install -qy nmap && \
    apt install -qy software-properties-common && \
    apt install -qy python3-pip && \
    apt install -qy curl && \
# Install a basic SSH server
    apt install -qy openssh-server && \
    sed -i 's|session    required     pam_loginuid.so|session    optional     pam_loginuid.so|g' /etc/pam.d/sshd && \
    mkdir -p /var/run/sshd
# Generate ssh key in root
RUN ssh-keygen -q -t rsa -N '' -f /id_rsa
# Create new CAMM user
RUN adduser --gecos "" --disabled-password --quiet CAMM && \
        echo "CAMM:CAMM" | chpasswd && \
    mkdir /home/CAMM/.m2 && \
        mkdir /home/CAMM/.ssh

RUN chown -R CAMM:CAMM /id_rsa.pub && \
    chown -R CAMM:CAMM /id_rsa && \
    chmod 0755 /id_rsa && \
    chown 0755 /id_rsa.pub && \
    chown -R CAMM:CAMM /home/CAMM/.m2/ && \
    chown -R CAMM:CAMM /home/CAMM/.ssh/

# Put CAMM Files in place
RUN git clone https://github.com/madeofpendletonwool/CAMM.git && \
    cp -R CAMM /data

WORKDIR /usr/src/app
COPY environprinter.py ./
CMD [ "python3", "./environprinter.py" ]