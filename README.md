# County eCitizen — Public Service Request System

A mini eCitizen-style portal for reporting county issues (streetlights, water,
garbage, roads). Citizens submit requests with photos; admins track, assign, and
resolve them, with a live analytics dashboard.

## Stack
- Django 5 · PostgreSQL · Bootstrap 5 · Crispy Forms · Pillow

## Quick start
```bash
sudo apt install postgresql libpq-dev python3-venv
sudo -u postgres psql -c "CREATE DATABASE county_ecitizen;"
sudo -u postgres psql -c "CREATE USER county_admin WITH PASSWORD 'secure_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE county_ecitizen TO county_admin;"

python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
