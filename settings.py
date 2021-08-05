import os
from dotenv import load_dotenv, find_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(find_dotenv())

FLASK_ENV = os.getenv('FLASK_ENV')
DEBUG = FLASK_ENV == 'development'
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'telzir.db')
# SQLALCHEMY_DATABASE_URI = 'sqlite:////telzir.db'
SECRET_KEY = 'Telzir-Quotation-FaleMais'
SQLALCHEMY_TRACK_MODIFICATIONS = False
