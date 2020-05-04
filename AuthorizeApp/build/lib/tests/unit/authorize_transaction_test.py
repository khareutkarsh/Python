"""
This file is a unit test file which covers the unit tests for authorize_transaction.py
"""
from pyscripts.business_rules.authorize_transaction import AuthorizeTransaction
from pyscripts.business_rules.manage_account import ManageAccount
from pyscripts.util import logging_util

import json

logging = logging_util.get_logger()
auth_txn = AuthorizeTransaction()
mng_acc = ManageAccount()


def test_check_txn_acceptance_in_time_slot():
    auth_txn.transaction_dict = {"2019-02-13 10:02:00": {
        1: {"transaction": {"merchant": "Burger King", "amount": 10, "time": "2019-02-13T10:00:59.000Z"}},
        2: {"transaction": {"merchant": "Lidl", "amount": 30, "time": "2019-02-13T10:00:00.000Z"}},
        3: {"transaction": {"merchant": "Aldi", "amount": 20, "time": "2019-02-13T10:01:41.000Z"}}},
        "2019-02-13 11:02:00": {
            1: {"transaction": {"merchant": "National Rail", "amount": 20, "time": "2019-02-13T11:00:59.000Z"}}}}
    transaction_json_data = json.loads(
        '{"transaction": {"merchant": "Zalando", "amount": 10, "time": "2019-02-13T10:01:59.000Z"}}')
    acceptance_status = auth_txn.check_txn_acceptance_in_time_slot(transaction_json_data, logging)
    assert not acceptance_status

    transaction_json_data = json.loads(
        '{"transaction": {"merchant": "Zalando", "amount": 10, "time": "2019-02-13T11:01:59.000Z"}}')
    acceptance_status = auth_txn.check_txn_acceptance_in_time_slot(transaction_json_data, logging)
    assert acceptance_status


def test_check_similar_txn_already_in_time_slot():
    auth_txn.transaction_dict = {"2019-02-13 10:02:00": {
        1: {"transaction": {"merchant": "Burger King", "amount": 10, "time": "2019-02-13T10:00:59.000Z"}},
        2: {"transaction": {"merchant": "Lidl", "amount": 30, "time": "2019-02-13T10:00:00.000Z"}}},
        "2019-02-13 11:02:00": {
            1: {"transaction": {"merchant": "National Rail", "amount": 20, "time": "2019-02-13T11:00:59.000Z"}}}}
    transaction_json_data = json.loads(
        '{"transaction": {"merchant": "Burger King", "amount": 10, "time": "2019-02-13T10:01:59.000Z"}}')
    acceptance_status = auth_txn.check_similar_txn_already_in_time_slot(transaction_json_data, logging)
    assert acceptance_status

    transaction_json_data = json.loads(
        '{"transaction": {"merchant": "Aldi", "amount": 10, "time": "2019-02-13T10:01:59.000Z"}}')
    acceptance_status = auth_txn.check_similar_txn_already_in_time_slot(transaction_json_data, logging)
    assert not acceptance_status


def test_process_transaction():
    message = '{"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T10:00:00.000Z"}}'
    mng_acc.account_dict = {}
    transaction_dict = {}
    violated_transaction_dict = {}
    response_dict = auth_txn.process_transaction(message, mng_acc, logging)
    assert response_dict == '{"account": null, "violations": ["account-not-initialized"]}'

    message = '{"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T10:00:00.000Z"}}'
    mng_acc.account_dict = json.loads(
        '{"account": {"active-card": false, "available-limit": 100}, "violations": []}')
    auth_txn.transaction_dict = {}
    response_dict2 = auth_txn.process_transaction(message, mng_acc, logging)
    assert response_dict2 == '{"account": {"active-card": false, "available-limit": 100}, "violations": ["card-not-active"]}'

    message = '{"transaction": {"merchant": "Burger King", "amount": 120, "time": "2019-02-13T10:00:00.000Z"}}'
    mng_acc.account_dict = json.loads(
        '{"account": {"active-card": true, "available-limit": 100}, "violations": []}')
    auth_txn.transaction_dict = {}
    response_dict3 = auth_txn.process_transaction(message, mng_acc, logging)
    assert response_dict3 == '{"account": {"active-card": true, "available-limit": 100}, "violations": ["insufficient-limit"]}'

    message = '{"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T10:01:00.000Z"}}'
    mng_acc.account_dict = json.loads(
        '{"account": {"active-card": true, "available-limit": 80}, "violations": []}')
    auth_txn.transaction_dict = {"2019-02-13 10:02:00": {
        1: {"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T10:00:00.000Z"}}}}
    response_dict4 = auth_txn.process_transaction(message, mng_acc, logging)
    assert response_dict4 == '{"account": {"active-card": true, "available-limit": 80}, "violations": ["doubled-transaction"]}'

    message = '{"transaction": {"merchant": "Mc Donalds", "amount": 30, "time": "2019-02-13T10:01:53.000Z"}}'
    mng_acc.account_dict = json.loads(
        '{"account": {"active-card": true, "available-limit": 40}, "violations": []}')
    auth_txn.transaction_dict = {"2019-02-13 10:02:00": {
        1: {"transaction": {"merchant": "Burger King", "amount": 10, "time": "2019-02-13T10:00:59.000Z"}},
        2: {"transaction": {"merchant": "Lidl", "amount": 30, "time": "2019-02-13T10:00:00.000Z"}},
        3: {"transaction": {"merchant": "Aldi", "amount": 20, "time": "2019-02-13T10:01:00.000Z"}}}}
    response_dict4 = auth_txn.process_transaction(message, mng_acc, logging)
    assert response_dict4 == '{"account": {"active-card": true, "available-limit": 40}, "violations": ["high-frequency-small-interval"]}'
