# Simple sshd server container

FROM ubuntu:14.04
MAINTAINER Kei Nohguchi <kei@nohguchi.com>

RUN apt-get update && apt-get install -y openssh-server
RUN mkdir /var/run/sshd

# Create admin account, so that we can share the Ansible operation with OpenSwitch
RUN useradd -m admin

# Allow password-less sudo
RUN sed -i 's@%admin ALL=(ALL) ALL@%admin ALL=(ALL) NOPASSWD:ALL@' /etc/sudoers

# Copy the ssh public key
RUN mkdir /home/admin/.ssh
COPY id_rsa.pub /home/admin/.ssh/authorized_keys
RUN chown -R admin /home/admin/.ssh
RUN chmod 0700 /home/admin/.ssh
RUN chmod 0400 /home/admin/.ssh/authorized_keys

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' - /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

EXPOSE 22
