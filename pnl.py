from datetime import datetime
from tabulate import tabulate

import config
from gateio import Gateio

sum_pnl = 0
for user in config.users.values():
    if not user['autotrade']:
        continue
    gateio = Gateio(user['gateio_key'], user['gateio_secret'])
    now = datetime.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    unixtime_start_of_month = int(start_of_month.timestamp())
    history = gateio.get_positions_history(unixtime_start_of_month)
    history_table_data = []
    for position in history:
        dt = datetime.fromtimestamp(position['time'])
        history_table_data.append([position['contract'],position['long_price'], position['short_price'], dt, position['pnl']])
        sum_pnl += float(position['pnl'])

history_table_data.reverse()
print(tabulate(history_table_data, headers=['PAIR', 'OPEN', 'CLOSE', 'DATE', 'PNL'], tablefmt='orgtbl'))
print(f'Total PNL: {sum_pnl}')