#!/bin/bash

# Start MySQL server
service mysql start

# Ensure you got the latest pcapoptikon version
cd /opt/pcapoptikon
git pull origin master
python manage.py migrate

# Update suricata rules
oinkmaster -C /etc/oinkmaster.conf -o /etc/suricata/rules

# Start Suricata
/usr/bin/suricata -c /etc/suricata/suricata.yaml --unix-socket >/dev/null 2>&1 &

# Start the pcapoptikon HTTP server
/usr/bin/python /opt/pcapoptikon/manage.py runserver 0.0.0.0:8000 >/var/log/pcapoptikon_web.log 2>&1 &

# Start the pcapoptikon daemon
/usr/bin/python /opt/pcapoptikon/manage.py run_daemon >/var/log/pcapoptikon_daemon.log 2>&1 &

# Give a hint about how to use
echo "Running on: http://"$(hostname -i)":8000/"

# Run oinkmaster every 24 hours and send SIGUSR2 to Suricata to make it reload the rules
while true; do
    sleep 60 * 60 * 24
    oinkmaster -C /etc/oinkmaster.conf -o /etc/suricata/rules
    killall -SIGUSR2 suricata
done
