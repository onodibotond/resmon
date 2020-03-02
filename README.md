DESCRIPTION
---------------------------------------
This is a resource (RAM usage) monitor application written in Python3.
It works as a linux service which is fully configurable, with parameters like:
 - % of ram used when to collect data
 - % of usage so the data about apps to be collected
 - collect full data about or just light data the specific apps
 - time interval to check the usage
 - other

PRE-REQUISITE
---------------------------------------
- python3 (# apt-get install python3)
- pip3    (# apt-get install python3-pip)
- psutil  (# pip3 install psutil)


INSTALL
---------------------------------------
- tar -xvf resmon.tar.gz
- cd resmon
- ./install.sh
