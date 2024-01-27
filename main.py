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

print_with_color("cyan", "MeraBot is running...")

# initialization
indicator_check = fetch_all_indicators(client)
if (indicator_check.price < indicator_check.ema_100):
    do_not_enter_long = True
    print_with_color("yellow", "LONG BLOCKED")
else:
    do_not_enter_short = True
    print_with_color("yellow", "SHORT BLOCKED")

while True:
    try:
        sleep(10)
        indicator_check = fetch_all_indicators(client)

        if not (on_long or on_short):
            if (not do_not_enter_long) and (indicator_check.macd_12 > indicator_check.macd_26) and \
                (indicator_check.macd_12 < 0) and (indicator_check.rsi_6 > 50) and \
                (indicator_check.price < indicator_check.ema_100):
                do_not_enter_short = False
                do_not_enter_long = True
                tp_price, sl_price = enter_long(client)
                print_with_color("yellow", "Entered LONG Current: " + 
                    str(round(indicator_position.price, 2)) + " TP_PRICE: " + str(round(tp_price, 2)) + 
                    " SL_PRICE: " + str(round(sl_price, 2)))
                on_long = True
                print_position_message(indicator_position, predictions[3])
            elif (not do_not_enter_short) and (indicator_check.macd_12 < indicator_check.macd_26) and \
                (indicator_check.macd_12 > 0) and (indicator_check.rsi_6 < 50) and \
                (indicator_check.price > indicator_check.ema_100):
                do_not_enter_long = False
                do_not_enter_short = True
                tp_price, sl_price = enter_short(client)
                print_with_color("yellow", "Entered SHORT Current: " + 
                    str(round(indicator_position.price, 2)) + " TP_PRICE: " + str(round(tp_price, 2)) + 
                    " SL_PRICE: " + str(round(sl_price, 2)))
                on_short = True
                
        else:
            if (on_long and  indicator_check.price > tp_price) or \
                  (on_short and indicator_check.price < tp_price):
                close_position(True)
            elif (on_long and indicator_check.price < sl_price) or \
                  (on_short and indicator_check.price > sl_price):
                close_position(False)

    except Exception as e:
        error_message = str(e)
        print_with_color("yellow", error_message)
