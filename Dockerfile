###################################
## IMAGE SETUP
###################################
FROM ubuntu:15.10
MAINTAINER cgstudiomap <cgstudiomap@gmail.com>
ENV PROJECT_HOME=/opt/cgstudiomap
ENV LOCAL_SHARE=/home/cgstudiomap/.local/share/Odoo/
VOLUME [ $PROJECT_HOME, LOCAL_SHARE]

# To avoid errors like debconf: unable to initialize frontend: Dialog
# See http://askubuntu.com/questions/506158/unable-to-initialize-frontend-dialog-when-using-ssh
ENV DEBIAN_FRONTEND=noninteractive

ADD requirements_apt.txt /

RUN apt-get update && \
    apt-get upgrade -yq && \
    apt-get install -y $(cat /requirements_apt.txt)

RUN rm /usr/bin/python && \
    ln -s /usr/bin/python2.7 /usr/bin/python

RUN pip install pip --upgrade

RUN useradd -m -s /bin/bash cgstudiomap
EXPOSE 8069 8072

USER cgstudiomap
WORKDIR $PROJECT_HOME
