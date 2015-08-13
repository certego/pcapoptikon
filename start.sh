#!/bin/bash
/usr/bin/suricata -c /etc/suricata/suricata.yaml --unix-socket >/dev/null 2>&1 &
/usr/bin/python /opt/pcapoptikon/manage.py runserver 0.0.0.0:8000 >/dev/null 2>&1 &
/usr/bin/python /opt/pcapoptikon/manage.py run_daemon >/dev/null 2>&1
