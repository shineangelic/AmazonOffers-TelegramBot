import logging
from telegram import Bot
from consts import *
import asyncio

logging.basicConfig(level=logging.INFO)

async def send_test_msg(message):
    # report the message
    
    bot = Bot(TOKEN)
    await bot.initialize()
    logging.info(f'{5 * "*"} Telegram bot init done {5 * "*"}')
    await bot.send_message(CHANNEL_NAME, message,parse_mode='HTML')
# create and execute coroutine


if __name__ == "__main__":
    # Create the bot instance
    logging.info(f'{5 * "*"} Telegram bot async message {5 * "*"}')
   
    asyncio.run(send_test_msg('Hi from a <b>shine</b> test'))
    