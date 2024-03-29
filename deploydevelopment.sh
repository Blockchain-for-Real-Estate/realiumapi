#!/bin/sh     
sudo git pull origin development
sudo pip3 install -r requirements.txt
cd djangoapi/realiumapi
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic
sudo systemctl restart nginx
sudo systemctl restart gunicorn