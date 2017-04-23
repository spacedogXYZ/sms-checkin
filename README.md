# SMS Check In

A simple check in application using SMS to engage participants at an event. Sends prompts before the start time to confirm attendance, and afterwards to rate the event.

# Developers

## Getting Started
* Install Python with pip and virtual environments
* Install requirements `pip install -r requirements/development.txt`

## Run Migrations
`python manage.py migrate`
`python manage.py createsuperuser`

## Run Server
`python manage.py runserver`
Open http://localhost:8000/

# Deployment

## Heroku
- Postgres
- Redis
- WhiteNoise

## Twilio
- Messaging