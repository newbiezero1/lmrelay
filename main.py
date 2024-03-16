import time
import sys
import json

import config
from discord_client import DiscordClient
import fun
from notifyer import Notifyer


def check_trades(trader: str):
    """Check new trades and make trade"""
    all_messages = client.fetch_messages(config.traders_channels[trader])
    new_message = fun.check_new_message(all_messages, config.files_list[trader])
    if new_message['content']:
        for user in config.users.values():
            notifyer = Notifyer(user["tg_chat_id"])
            notifyer.send_message(new_message['content'])
            with open(config.last_tweet_file, 'w') as f:
                f.write(json.dumps({'tweet_id': 1, 'time': int(time.time())}))


#time.sleep(10)
client = DiscordClient(config.discord_token)
# trade section
check_trades('loma')
