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
date = None

# Global Functions
def close_position(isTP):
    global on_long
    global on_short
    global tp_count
    global sl_count
    global csv_path_result
    global date

    state = "" 
    
    if (on_long and isTP) or (on_short and (not isTP)): 
        state = "LONG"
    elif (on_long and (not isTP)) or (on_short and isTP):
        state = "SHORT"

    save_result(csv_path_result, date, state, "LONG" if on_long else "SHORT")

    on_long = False
    on_short = False

    if isTP:
        tp_count = tp_count + 1
        print_with_color("green", "Position closed with TP")
        print_with_color("yellow", "TP: " + str(tp_count) + " SL: " + 
              str(sl_count) + " Win-Rate: " + calculateWR(tp_count, sl_count))
    else:
        sl_count = sl_count + 1
        print_with_color("red", "Position closed with SL")
        print_with_color("yellow", "TP: " + str(tp_count) + " SL: " + 
            str(sl_count) + " Win-Rate: " + calculateWR(tp_count, sl_count))

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
                date = indicator_check.date
                tp_price, sl_price = enter_long(client)
                print()
                print_with_color("yellow", "Entered LONG Current: " + 
                    str(round(indicator_check.price, 2)) + " TP_PRICE: " + str(round(tp_price, 2)) + 
                    " SL_PRICE: " + str(round(sl_price, 2)))
                on_long = True
                print_position_message(indicator_check, "LONG")
            elif (not do_not_enter_short) and (indicator_check.macd_12 < indicator_check.macd_26) and \
                (indicator_check.macd_12 > 0) and (indicator_check.rsi_6 < 50) and \
                (indicator_check.price > indicator_check.ema_100):
                do_not_enter_long = False
                do_not_enter_short = True
                date = indicator_check.date
                tp_price, sl_price = enter_short(client)
                print()
                print_with_color("yellow", "Entered SHORT Current: " + 
                    str(round(indicator_check.price, 2)) + " TP_PRICE: " + str(round(tp_price, 2)) + 
                    " SL_PRICE: " + str(round(sl_price, 2)))
                on_short = True
                print_position_message(indicator_check, "LONG")

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
