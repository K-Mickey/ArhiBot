import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from bin.ect import cfg

dp = Dispatcher()

logging.basicConfig(level=logging.INFO, stream=sys.stdout)


async def run() -> None:
    bot = Bot(cfg.BOT_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)
