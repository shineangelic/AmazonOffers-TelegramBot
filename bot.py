from sre_parse import CATEGORIES
from typing import Dict, List
import telegram
from amazon_api import search_items
from create_messages import create_item_html
import time
from datetime import datetime
from itertools import chain
import random
from consts import *
import logging
import asyncio

logging.basicConfig(level=logging.INFO)

# ********** Author: Samir Salman **********


# Search keywords definition
"""
A dictionary with {CATEGORY_NAME: [<LIST OF THE CATEGORY KEYWORDS>]}
"""

categories = {
    #"HealthPersonalCare": [
    #    "Anal plug",
    #],
    "ToysAndGames": [
        "Kyosho", "Tamiya", "HPI"
    ]

}


def is_active() -> bool:
    now = datetime.now().time()
    return MIN_HOUR < now.hour < MAX_HOUR


async def asynch_dequeue_messages(list_of_struct: List[str]) -> List[str]:
    
    await bot.send_message(
        chat_id=CHANNEL_NAME,
        text=list_of_struct[0],
        reply_markup=list_of_struct[1],
        parse_mode='HTML',
    )
    logging.info('Posted message %s', list_of_struct[0])
    return list_of_struct[2:]


# run bot function
def run_bot(bot: telegram.Bot, categories: Dict[str, List[str]]) -> None:
    # start loop
    while True:
        try:
            items_full = []
            # iterate over keywords
            for category in categories:
                for keyword in categories[category]:
                    # iterate over pages
                    for page in range(1, 3):
                        logging.info(f'{5 * "*"} Paged search %s:%s PAGINA:%i{5 * "*"}',category ,keyword,page)
                        items = search_items(keyword, category, item_page=page)
                        # api time limit for another http request is 1 second
                        time.sleep(1)
                        items_full.extend(items)

            logging.info(f'{5 * "*"} Requests Completed {5 * "*"}')

            # shuffling results times
            random.shuffle(items_full)

            # creating html message, you can find more information in create_messages.py
            res = create_item_html(items_full)

            if (len(res)<= 3):
                logging.warning(f'{5 * "*"} Nothing to post {5 * "*"}')

            # while we have items in our list
            while len(res) > 3:

                # if bot is active
                if is_active():
                    try:
                        # Sending two consecutive messages
                        logging.info(f'{5 * "*"} Sending posts to channel {5 * "*"}')
                        asyncio.run(asynch_dequeue_messages(res))
                        #res = send_consecutive_messages(res)

                    except Exception as e:
                        logging.error(e)
                        res = res[2:]
                        continue

                    # Sleep for PAUSE_MINUTES
                    logging.info(
                        f'{5 * "*"} BOT sleeping ...  {PAUSE_MINUTES} {5 * "*"}'
                    )
                    time.sleep(60 * PAUSE_MINUTES)

                else:
                    # if bot is not active
                    logging.info(
                        f'{5 * "*"} Inactive Bot, between  {MIN_HOUR}AM and {MAX_HOUR}PM {5 * "*"}'
                    )
                    time.sleep(60 * 5)

        except Exception as e:
            logging.info(e)


if __name__ == "__main__":
    # Create the bot instance
    bot = telegram.Bot(token=TOKEN)
     
    
    # running bot
    run_bot(bot=bot, categories=categories)
