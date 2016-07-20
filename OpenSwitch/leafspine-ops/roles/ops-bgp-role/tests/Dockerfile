FROM keinohguchi/openswitch:2016060112

MAINTAINER Kei Nohguchi <kei@nohguchi.com>

# Copy the ssh public key
RUN mkdir /home/admin/.ssh
COPY id_rsa.pub /home/admin/.ssh/authorized_keys
RUN chown -R admin:ops_admin /home/admin/.ssh
RUN chmod 0700 /home/admin/.ssh
RUN chmod 0400 /home/admin/.ssh/authorized_keys

# Interface related utility
RUN mkdir /home/admin/bin
COPY ops-if-netns.sh /home/admin/bin/
RUN chmod 0544 /home/admin/bin/ops-if-netns.sh

# Ports to be exposed to the Ansible control machines
EXPOSE 22
