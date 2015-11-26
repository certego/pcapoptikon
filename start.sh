#!/bin/bash
#
# start.sh
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA  02111-1307  USA
#
# Author:   Pietro Delsante <p.delsante@certego.net>
#           www.certego.net
#

# Send all output (stdout + stderr) to a log file
exec > >(tee /var/log/pcapoptikon_startup.log)
exec 2>&1

# Start MySQL server
echo "Starting MySQL..."
service mysql start

# Ensure you got the latest pcapoptikon version
echo "Pulling PCAPOptikon repo..."
cd /opt/pcapoptikon
git pull origin master
python manage.py migrate

# Adding local.rules to suricata.yaml if it's not there already
touch /etc/suricata/rules/local.rules
[ $(grep "local.rules" /etc/suricata/suricata.yaml | wc -l) -eq 0 ] && sed -i '/tor.rules/ a\
 - local.rules' /etc/suricata/suricata.yaml

# ETPro format: https://rules.emergingthreats.net/<code>/suricata/etpro.rules.tar.gz
if [ $(echo $1 | egrep '^[0-9]{16}$' | wc -l) -eq 1 ]; then
    echo "Using supplied OinkCode to set up ETPro ruleset in oinkmaster"
    sed -ir "s|^url = http://rules.emergingthreats.net/open/suricata/emerging.rules.tar.gz|url = https://rules.emergingthreats.net/$1/suricata/etpro.rules.tar.gz|" /etc/oinkmaster.conf
else
    echo "Using default ET Open ruleset (to change this, please pass your ETPro oinkcode as the first param to $0"
fi

# Update suricata rules
echo "Running OinkMaster to update signatures..."
oinkmaster -C /etc/oinkmaster.conf -o /etc/suricata/rules

# Start Suricata
echo "Starting Suricata..."
rm -f /var/run/suricata.pid
/usr/bin/suricata -c /etc/suricata/suricata.yaml --unix-socket --pidfile /var/run/suricata.pid >/dev/null 2>&1 &

# Start the pcapoptikon HTTP server
echo "Starting the PCAPOptikon HTTP Server..."
/usr/bin/python /opt/pcapoptikon/manage.py runserver 0.0.0.0:8000 >/var/log/pcapoptikon_web.log 2>&1 &
echo $! > /var/run/pcapoptikon-http.pid

# Start the pcapoptikon daemon
echo "Starting the PCAPOptikon worker daemon..."
/usr/bin/python /opt/pcapoptikon/manage.py run_daemon >/var/log/pcapoptikon_daemon.log 2>&1 &
echo $! > /var/run/pcapoptikon-daemon.pid

# Give a hint about how to use
echo "Running on: http://"$(hostname -i)":8000/"
echo "Username: admin"
echo "Api-Key: "$(mysql -e 'SELECT `key` FROM tastypie_apikey WHERE user_id = (SELECT id FROM auth_user WHERE username = '"'"'admin'"'"');' pcapoptikon)

# Run oinkmaster every 24 hours and restart suricata and pcapoptikon daemon to reload the rules
while true; do
    sleep $(expr 60 \* 60 \* 24)
    oinkmaster -C /etc/oinkmaster.conf -o /etc/suricata/rules
    kill $(cat /var/run/pcapoptikon-daemon.pid)
    sleep 5
    rm -f /var/run/pcapoptikon-daemon.pid
    kill $(cat /var/run/suricata.pid)
    sleep 5
    rm -f /var/run/suricata.pid
    /usr/bin/suricata -c /etc/suricata/suricata.yaml --unix-socket --pidfile /var/run/suricata.pid >/dev/null 2>&1 &
    /usr/bin/python /opt/pcapoptikon/manage.py run_daemon >/var/log/pcapoptikon_daemon.log 2>&1 &
    echo $! > /var/run/pcapoptikon-daemon.pid
done
