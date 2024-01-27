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