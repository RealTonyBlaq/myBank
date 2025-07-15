from dotenv import load_dotenv, find_dotenv
from os import getenv
import redis
from typing import Optional


# Load environment variables from .env file
load_dotenv(find_dotenv())

expiry_time = int(getenv("REDIS_EXPIRY_TIME", 4))  # in minutes


class Cache:
    """ Defines a Cache class that stores and retrieves items from storage """

    def __init__(self) -> None:
        """ Initializes the Cache class with a Redis instance """
        self.client = redis.Redis()

    def get(self, key: str) -> Optional[str]:
        """ Retrieves value using a key """
        value = self.client.get(key)

        return value.decode('utf-8') if value else None # type: ignore

    def set(self, key: str, value: str, expires_after: int) -> None:
        """ Set/store a value using a key and an expiry time coverted to seconds """
        self.client.setex(key, 60 * expires_after, value)

    def delete(self, key: str) -> None:
        """ Deletes a key-value pair """
        self.client.delete(key)
