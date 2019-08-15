from libs.bot_async_messaging import AsyncBot
from libs.updater_async import AsyncUpdater
from libs.database import Conn

from config import PRODUCTION_TOKEN, request_kwargs, psql_credentials, PORT

import multiprocessing
import pytz
import tzlocal

#

castles = ['🍆', '🍁', '☘', '🌹', '🐢', '🦇', '🖤']

conn = Conn(psql_credentials)
conn.start()
cursor = conn.cursor()

bot = AsyncBot(token=PRODUCTION_TOKEN, workers=16, request_kwargs=request_kwargs)
updater = AsyncUpdater(bot=bot)

dispatcher = updater.dispatcher
job = updater.job_queue

bot.dispatcher = dispatcher

mobs_queue = multiprocessing.Queue()


CHAT_WARS_ID = 265204902

processing = True

moscow_tz = pytz.timezone('Europe/Moscow')
try:
    local_tz = tzlocal.get_localzone()
except pytz.UnknownTimeZoneError:
    local_tz = pytz.timezone('Europe/Andorra')
