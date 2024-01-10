API_DOCUMENTATION = https://documenter.getpostman.com/view/28287527/2s9YsKgXyM

to create RiderProfile and DriverProfile you need follow few steps
python manage.py shell,
from general.functions import CreateRider,
CreateRider('name','password'),
from general.functions import CreateDriver,
CreateRider('name','password'),

Install Redis in the system and run the redis portal for the realtime location updtaion using Channels
Install the requirements and configure .env as per postgres db credential
