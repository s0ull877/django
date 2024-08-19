import os
from aiogram import Bot
from pathlib import Path
import redis

REDIS = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), decode_responses=True)

bot = Bot(token=os.getenv('TOKEN'))

BASE_DIR = Path()

AVAILABLE_PHONE = ['79', '77', '37', '38']