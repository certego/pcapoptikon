#!/usr/bin/expect -f
spawn python manage.py createsuperuser --username admin --email user@example.com
expect "Password: "
send "admin\r"
expect "Password (again): "
send "admin\r"
