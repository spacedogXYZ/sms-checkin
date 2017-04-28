# SMS Check In

A simple check in application using SMS to engage participants at an event. Sends prompts before the start time to confirm attendance, and afterwards to rate the event.

# Developers

## Getting Started
- Install Python with pip and virtual environments
- Install requirements `pip install -r requirements/development.txt`

## Run Migrations
- `python manage.py migrate`
- `python manage.py createsuperuser`

## Run Server
- `python manage.py runserver`
- Open http://localhost:8000/

# Deployment
- set environment variables:
	- SECRET_KEY=[some long random string](https://docs.djangoproject.com/en/1.11/ref/settings/#secret-key)
	- DJANGO_SETTINGS_MODULE=sms_checkin.settings.production

## Heroku
- Postgres
- Redis
- WhiteNoise

## Twilio
- Messaging
-- setup your desired phone number to point to https://APP.herokuapp.com/sms/messages/