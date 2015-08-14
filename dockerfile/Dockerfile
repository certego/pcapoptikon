# This is a Dockerfile for creating a Thug https://github.com/buffer/thug Container from the latest
# Ubuntu base image. This is known bo be working on Ubuntu 14.04. It should work on any later version
# This is a full installation of Thug including all optional packages used for distributed operation
FROM ubuntu:14.04
MAINTAINER p.delsante@certego.net
ENV LC_ALL C
ENV DEBIAN_FRONTEND noninteractive
EXPOSE 8000

RUN apt-get update && apt-get -y dist-upgrade && apt-get -y install \
            cpanminus \
            git \
            libmysqlclient-dev \
            libssl-dev \
            mysql-common \
            mysql-client \
            mysql-server \
            oinkmaster \
            python-dev \
            python-mysqldb \
            python-software-properties \
            python-pip \
            software-properties-common
        
RUN add-apt-repository -y ppa:oisf/suricata-stable && apt-get update && apt-get -y install suricata

RUN sed -ir '/^# more information.$/ a\
url = http://rules.emergingthreats.net/open/suricata/emerging.rules.tar.gz' /etc/oinkmaster.conf

RUN sed -ir 's|^classification-file: /etc/suricata/classification.config$|classification-file: /etc/suricata/rules/classification.config|' /etc/suricata/suricata.yaml
RUN sed -ir 's|^reference-file: /etc/suricata/reference.config$|classification-file: /etc/suricata/rules/reference.config|' /etc/suricata/suricata.yaml
RUN sed -ir 's|#- rule-reload: true|- rule-reload: true|' /etc/suricata/suricata.yaml
RUN touch /etc/suricata/threshold.config
        
RUN git clone https://github.com/pdelsante/pcapoptikon.git /opt/pcapoptikon && \
        pip install -r /opt/pcapoptikon/requirements.txt
        
RUN service mysql start && \
        mysqladmin create pcapoptikon && \
        cd /opt/pcapoptikon/ && \
        python manage.py migrate --noinput
        
VOLUME ["/var/lib/mysql"]

CMD ["/opt/pcapoptikon/start.sh"]
