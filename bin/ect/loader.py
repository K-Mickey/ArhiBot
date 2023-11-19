import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from bin.base import main_commands
from bin.ect import cfg


logging.basicConfig(level=logging.INFO, stream=sys.stdout)


async def run() -> None:
    dp = Dispatcher()
    dp.include_routers(
        main_commands.router,
    )
    bot = Bot(cfg.BOT_TOKEN, parse_mode=ParseMode.HTML)

    await dp.start_polling(bot)
