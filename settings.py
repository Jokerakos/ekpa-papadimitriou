#demo/settings.py
from os import environ 

SECRET_KEY = environ.get('connectiondata')