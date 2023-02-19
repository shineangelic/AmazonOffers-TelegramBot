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
    "HealthPersonalCare": [
        "Rasoio",
    ],
    "ToysAndGames": [
        "Kyosho", "Tamiya", "HPI"
    ],
    "MusicalInstruments":[
        "Basso", "Chitarra acustica"
    ],
    "Electronics":[
        "Nvidia GeForce", "Intel i9"
    ],
    "Industrial":[
        "Chair", "Gaming desk"
    ],
    "VideoGames":[
        "Zelda", "Nintendo"
    ]

}


def is_active() -> bool:
    now = datetime.now().time()
    return MIN_HOUR <= now.hour <= MAX_HOUR


async def asynch_dequeue_messages(list_of_struct: List[str]) -> List[str]:
    
    await bot.send_message(
        chat_id=CHANNEL_NAME,
        text=list_of_struct[0],
        reply_markup=list_of_struct[1],
        parse_mode='HTML',
    )
    logging.debug('Posted message %s', list_of_struct[0])
    return list_of_struct[2:]


# run bot function
def run_bot(bot: telegram.Bot, categories: Dict[str, List[str]]) -> None:
    # start loop
    while True:
        try:
            items_full = []
            num_cat=0
             
            # iterate over keywords
            for category in categories:
                num_cat+=1
                numk=0
                for keyword in categories[category]:
                    numk+=1
                    numpage=0
                    # iterate over pages
                    for page in range(1, MAX_PAGES):
                        numpage+=1
                        perc = ((numk+numpage) * 100) / (len(categories[category]*MAX_PAGES))
                        logging.info(f'{5 * "*"} Progresso ricerca %i:%i %f%%{5 * "*"}',num_cat,len(categories),perc)
                        items = search_items(keyword, category, item_page=page)
                        # api time limit for another http request is 1 second
                        time.sleep(1)
                        items_full.extend(items)

            logging.info(f'{5 * "*"} Ricerca completata. %i items disponibili {5 * "*"}',len(items_full))

            # shuffling results times
            random.shuffle(items_full)

            # creating html message, you can find more information in create_messages.py
            res = create_item_html(items_full)

            if (len(res)<= 3):
                logging.warning(f'{5 * "*"} NIENTE DA POSTARE! {5 * "*"}')

            # while we have items in our list
            while len(res) > 3:

                # if bot is active
                if is_active():
                    try:
                        # Sending two consecutive messages
                        logging.info(f'{5 * "*"} Invio post in corso {5 * "*"}')
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
                        f'{5 * "*"} BOT INATTIVO, between  {MIN_HOUR}AM and {MAX_HOUR}PM {5 * "*"}'
                    )
                    time.sleep(60 * 5)

        except Exception as e:
            logging.error(e)


if __name__ == "__main__":
    # Create the bot instance
    bot = telegram.Bot(token=TOKEN)
     
    
    # running bot
    run_bot(bot=bot, categories=categories)
