#!/bin/bash
#This is the install script
#It has to be executed as root user 

mkdir -p /etc/resmon/
mkdir -p /opt/resmon/archives/

cp -f src/*.py /opt/resmon/
cp -f conf/* /etc/resmon/

cp resmon.service /etc/systemd/system/resmon.service
systemctl enable resmon.service
systemctl start resmon.service
