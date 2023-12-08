import logging

from bin.ect import cfg


async def send_message(user_id: int, message: str) -> None:
    from bin.ect.loader import bot
    await bot.send_message(user_id, message)


def create_logger() -> None:
    logging.basicConfig(level=cfg.LOG_LEVEL, format=cfg.LOG_FORMATTER, filename=cfg.LOG_PATH)
