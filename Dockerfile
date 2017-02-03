FROM ubuntu:16.10
RUN apt-get -y update
RUN apt-get -y install net-tools openssh-server python ansible
RUN update-ca-certificates

ADD docker/ansible.cfg /root/.ansible.cfg
RUN mkdir -p /data/src /data/src/ansible /data/src/app /data/src/web /data/src/templates /data/src/certs
ADD docker/hosts /data/src/ansible/
ADD ansible/ /data/src/ansible/
ADD app/ /data/src/app/
ADD web/ /data/src/web/
ADD certs/ /data/src/certs/

WORKDIR /data/src/ansible
RUN ansible-playbook -i hosts all.yaml
RUN ansible-playbook -i hosts db.yaml
RUN ansible-playbook -i hosts app.yaml
RUN ansible-playbook -i hosts web.yaml
RUN ansible-playbook -i hosts tex.yaml

WORKDIR /data

ADD docker/run.sh /root/run.sh
CMD /bin/bash --rcfile /root/run.sh
