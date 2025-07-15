from dotenv import load_dotenv, find_dotenv
from .mongo_db import MongoDB
from .redis_db import Cache
from os import getenv


DB_HOST = getenv('DB_HOST', 'localhost')
DB_PORT = int(getenv('DB_PORT', 27017))
DB_NAME = getenv('DB_NAME', 'myBank')

db = MongoDB(DB_HOST, DB_PORT, DB_NAME)
cache = Cache()
