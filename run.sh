#!/usr/bin/env bash
cd /webapps/payday/
pip3 install -r requirements.txt
export DJANGO_SETTINGS_MODULE="system.settings"
python3 manage.py collectstatic --noinput
python3 manage.py migrate --noinput
systemctl restart payday
systemctl restart nginx
