import time
import json

import config
from discord_client import DiscordClient
import fun
from notifyer import Notifyer
from gateio import Gateio
from loma import Loma


def check_trades(trader: str) -> None:
    """Check new trades and make trade"""
    all_messages = client.fetch_messages(config.traders_channels[trader])
    new_message = fun.check_new_message(all_messages, config.files_list[trader])
    if new_message['content']:
        for user in config.users.values():
            notifyer = Notifyer(user["tg_chat_id"])
            notifyer.send_message(f'*{trader} NEW MESSAGE:*', markdown=True)
            notifyer.send_message(new_message['content'])
            with open(config.last_tweet_file, 'w') as f:
                f.write(json.dumps({'tweet_id': 1, 'time': int(time.time())}))
            loma = Loma()
            entries = loma.get_entry_levels(new_message['content'])
            if entries:
                message = '''Entry Levels:\n'''
                for entry in entries:
                    message += f'L: {entry}\n'
                notifyer.send_message(message)


def check_sl_alert(trader: str) -> None:
    all_messages = client.fetch_messages(config.alerts_channels[trader])
    new_message = fun.check_new_message(all_messages, config.files_list[trader+'_alerts'])
    if new_message['content']:
        loma = Loma()
        loma.parse_alert(new_message['content'])

        saved_sl = json.loads(fun.get_content_file(config.files_list[trader+'_sl']))
        for sl_item in saved_sl:
            if sl_item['pair'] == loma.alert['pair']:
                saved_sl.remove(sl_item)

        saved_sl.append(loma.alert)
        fun.set_content_file(config.files_list[trader+'_sl'], json.dumps(saved_sl))


def check_sl_true(sl_data: dict, gateio: object) -> None:
    candless = gateio.get_bars(sl_data['pair'], sl_data['time'])
    last_bar = candless[-2]
    if last_bar['c'] < sl_data['sl']:
        gateio.close_position(sl_data['pair'])
        print('close_position')

def check_positions(trader: str) -> None:
    saved_sl = json.loads(fun.get_content_file(config.files_list[trader + '_sl']))
    if not saved_sl:
        return
    for user in config.users.values():
        if not user['autotrade']:
            continue
        gateio = Gateio(user['gateio_key'], user['gateio_secret'])
        positions = gateio.get_positions()
        for position in positions:
            if position['size'] == 0:
                continue
            for sl in saved_sl:
                if sl['pair']+'_USDT' == position['contract']:
                    check_sl_true(sl, gateio)

time.sleep(5)
client = DiscordClient(config.discord_token)
# trade section
check_trades('loma')
check_sl_alert('loma')
check_positions('loma')

check_trades('guru')