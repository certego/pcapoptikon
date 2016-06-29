#!/bin/bash
#
# reload.sh
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

function log() {
    echo "[$(date +'%y-%m-%d %H:%M:%S')] $@"
}

# Send all output (stdout + stderr) to a log file
exec > >(tee /var/log/pcapoptikon_reload.log)
exec 2>&1

# Update sid-msg.map
log "Updating sid-msg.map"
/usr/share/oinkmaster/create-sidmap.pl /etc/suricata/rules > /etc/suricata/rules/sid-msg.map

log "Stopping pcapoptikon's run_daemon and deleting pid file"
kill $(cat /var/run/pcapoptikon-daemon.pid)
sleep 5
rm -f /var/run/pcapoptikon-daemon.pid

log "Stopping suricata and deleting pid file"
kill $(cat /var/run/suricata.pid)
sleep 5
rm -f /var/run/suricata.pid

log "Starting up suricata and run_daemon again"
/usr/bin/suricata -c /etc/suricata/suricata.yaml --unix-socket --pidfile /var/run/suricata.pid >/dev/null 2>&1 &
/usr/bin/python /opt/pcapoptikon/manage.py run_daemon >/var/log/pcapoptikon_daemon.log 2>&1 &
log $! > /var/run/pcapoptikon-daemon.pid

log "Signatures reloaded"
