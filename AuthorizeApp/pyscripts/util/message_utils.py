"""
This file is a util which is used to perform message related operations
"""
import json
from datetime import datetime
import datetime


# Method to convert the json to string and vice-versa
from pyscripts.constants.app_constants import TRANSACTION_WINDOW_IN_MIN


def convert_to_string_to_json(message, message_type):
    if message_type == "STRING":
        return_json_message = json.loads(message)
        return return_json_message
    elif message_type == "JSON":
        return_str_message = json.dumps(message)
        return return_str_message


# Method to check the request type of the message
def get_request_type(message, logger):
    json_data = convert_to_string_to_json(message, "STRING")
    if 'account' in json_data:
        return "ACCOUNT"
    else:
        return "TRANSACTION"


# Method to retrieve transaction time key (2-min slots)
def get_transaction_time_key(txn_json_data):
    transaction_time_str = txn_json_data['transaction']['time']
    transaction_time = datetime.datetime.strptime(transaction_time_str[:-1], "%Y-%m-%dT%H:%M:%S.%f")
    remainder_min = transaction_time.minute % TRANSACTION_WINDOW_IN_MIN
    if remainder_min == 0:
        transaction_time_key = transaction_time - datetime.timedelta(0,
                                                                     transaction_time.second) + datetime.timedelta(
            0,
            TRANSACTION_WINDOW_IN_MIN*60)
    else:
        transaction_time_key = transaction_time - datetime.timedelta(0,
                                                                     transaction_time.second) + datetime.timedelta(
            0,
            remainder_min*60)
    return str(transaction_time_key)
