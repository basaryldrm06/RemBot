from binance.client import Client
from binanceAPI.position_utilities import enter_long, enter_short
from config import api_key, secret_key
from indicators.fetch_all_indicators import fetch_all_indicators
from data.io_utilities import print_with_color, calculateWR, print_position_message
from data.IndicatorData import IndicatorData
from time import sleep
from data.data_functions import save_position, save_result
import copy

# BinanceAPI Connection
client = Client(api_key, secret_key)

# csv path initialization
csv_path_result = "./data/rembot_result.csv"

# Global Variables
indicator_check = None
tp_count = 0
sl_count = 0
tp_price = 0
sl_price = 0
do_not_enter_long = False
do_not_enter_short = False
on_long = False
on_short = False


# initialization
indicator_check = fetch_all_indicators(client)
if (indicator_check.price < indicator_check.ema_100):
    do_not_enter_long = True
    print_with_color("yellow", "LONG BLOCKED")
else:
    do_not_enter_short = True
    print_with_color("yellow", "SHORT BLOCKED")