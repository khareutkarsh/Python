"""
This file is a unit test file which covers the unit tests for message_utils.py
"""
from pyscripts.util import logging_util, message_utils
import json

logging = logging_util.get_logger()


def test_get_request_type():
    message = '{"account": {"active-card": false, "available-limit": 100}}'
    request_type = message_utils.get_request_type(message, logging)
    assert request_type == 'ACCOUNT'

    message = '{"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T10:00:00.000Z"}}'
    request_type = message_utils.get_request_type(message, logging)
    assert request_type == 'TRANSACTION'



def test_get_transaction_time_key():
    json_data = json.loads(
        '{"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T10:02:20.000Z"}}')
    transaction_time_key = message_utils.get_transaction_time_key(json_data)
    assert transaction_time_key == '2019-02-13 10:04:00'



def test_convert_to_string_to_json():
    message = '{"account": {"active-card": false, "available-limit": 100}}'
    expected_message = json.loads(message)
    message_type = "STRING"
    return_message = message_utils.convert_to_string_to_json(message, message_type)
    assert return_message == expected_message

    expected_message = '{"account": {"active-card": false, "available-limit": 100}}'
    message = json.loads(expected_message)
    message_type = "JSON"
    return_message = message_utils.convert_to_string_to_json(message, message_type)
    assert return_message == expected_message
