import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '..', 'config.ini'))

# Database
DB_USER = config['database']['DB_USER']
DB_PASSWORD = config['database']['DB_PASSWORD']
DB_HOST = config['database']['DB_HOST']
DB_PORT = config['database']['DB_PORT']
DB_NAME = config['database']['DB_NAME']

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Auth
SECRET_KEY = config['auth']['SECRET_KEY']
ALGORITHM = config['auth']['ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = int(config['auth']['ACCESS_TOKEN_EXPIRE_MINUTES'])