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
	- create a new [Twilio messaging service](https://www.twilio.com/console/sms/dashboard) with Inbound Request URL https://APP.herokuapp.com/sms/messages/ as HTTP POST
	- connect one or more phone numbers to your new Twilio messaging service
	- set environment variables TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_MESSAGING_SID