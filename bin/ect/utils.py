async def send_message(user_id: int, message: str) -> None:
    from bin.ect.loader import bot
    await bot.send_message(user_id, message)