# Based on the deprecated ansible docker image:
#
# https://hub.docker.com/r/ansible/ubuntu14.04-ansible/
#
# especially, this Dockerfile:
#
# https://github.com/ansible/ansible-docker-base/blob/master/devel-ubuntu14.04/Dockerfile
#
FROM ubuntu:14.04

MAINTAINER Kei Nohguchi <kei@nohguchi.com>

# Copy the ssh private key
RUN mkdir /root/.ssh
ADD id_rsa /root/.ssh/id_rsa
RUN chmod 0700 /root/.ssh
RUN chmod 0400 /root/.ssh/id_rsa

# Required package(s)
RUN apt-get -y update && \
    apt-get install -y build-essential openssh-client git \
                       libssl-dev libffi-dev \
                       python-dev python-keyczar python-setuptools \
                       python-pkg-resources

# http://docs.ansible.com/ansible/intro_installation.html#running-from-source
RUN easy_install pip
# New paramiko requires cryptography, which depends on
# the hashlib.  The following line addresses some issue
# but not complete, hense, falls back to the old version
# of the paramiko-1.6.0 until I figure that out.
#RUN pip install cffi hashlib cryptography \
#                paramiko PyYAML Jinja2 httplib2 six
RUN pip install paramiko==1.16.0 PyYAML Jinja2 httplib2 six

# Prepare the ansible runtime
RUN mkdir -p /opt
WORKDIR /opt
RUN git clone https://github.com/ansible/ansible.git --recursive

# Ansible home
RUN mkdir -p /etc/ansible
WORKDIR /etc/ansible
ENV PATH /opt/ansible/bin:/bin:/usr/bin:/sbin:/usr/sbin
ENV PYTHONPATH /opt/ansible/lib
ENV ANSIBLE_LIBRARY /opt/ansible/library
