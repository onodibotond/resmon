#!/bin/bash

mkdir -p /etc/resmon/
mkdir -p /opt/resmon/startup/
mkdir -p /opt/resmon/archives/

cp -f src/*.py /opt/resmon/
cp -f src/startup/resmon.sh /opt/resmon/startup/
cp -f conf/* /etc/resmon/

cp -f resmon /etc/init.d/resmon
chmod +x /etc/init.d/resmon
update-rc.d resmon defaults

/etc/init.d/resmon start
