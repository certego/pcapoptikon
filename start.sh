#!/bin/bash

# Send all output (stdout + stderr) to a log file
exec > >(tee /var/log/pcapoptikon_startup.log)
exec 2>&1

# Start MySQL server
service mysql start

# Ensure you got the latest pcapoptikon version
cd /opt/pcapoptikon
git pull origin master
python manage.py migrate

#https://rules.emergingthreats.net/<code>/suricata/etpro.rules.tar.gz

if [ $(echo $1 | egrep '^[0-9]{16}$' | wc -l) -eq 1 ]; then
    echo "Using supplied OinkCode to set up ETPro ruleset in oinkmaster"
    sed -ir "s|^url = http://rules.emergingthreats.net/open/suricata/emerging.rules.tar.gz|url = https://rules.emergingthreats.net/$1/suricata/etpro.rules.tar.gz|"
else
    echo "Using default ET Open ruleset (to change this, please pass your ETPro oinkcode as the first param to $0"
fi

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
echo "Username: admin"
echo "Api-Key: "$(mysql -e 'SELECT `key` FROM tastypie_apikey WHERE user_id = (SELECT id FROM auth_user WHERE username = '"'"'admin'"'"');' pcapoptikon)

# Run oinkmaster every 24 hours and send SIGUSR2 to Suricata to make it reload the rules
while true; do
    sleep $(expr 60 \* 60 \* 24)
    oinkmaster -C /etc/oinkmaster.conf -o /etc/suricata/rules
    killall -SIGUSR2 suricata
done
