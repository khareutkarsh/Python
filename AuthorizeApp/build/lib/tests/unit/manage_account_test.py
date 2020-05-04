"""
This file is a unit test file which covers the unit tests for manage_account.py
"""
from pyscripts.business_rules.manage_account import ManageAccount
from pyscripts.util import logging_util
import json

logging = logging_util.get_logger()
mng_acc = ManageAccount()


def test_generate_violations():
    mng_acc.account_dict = {}
    violations_list = []
    acc_json_data = json.loads('{"account": {"active-card": true, "available-limit": 100}}')
    response_dict = mng_acc.generate_violations(violations_list, logging, acc_json_data)

    assert response_dict == '{"account": {"active-card": true, "available-limit": 100}, "violations": []}'

    mng_acc.account_dict = json.loads(response_dict)
    acc_json_data = json.loads('{"account": {"active-card": true, "available-limit": 300}}')
    violations_list = ["account-already-initialized"]
    response_dict2 = mng_acc.generate_violations(violations_list, logging, acc_json_data)
    assert response_dict2 == '{"account": {"active-card": true, "available-limit": 100}, "violations": ["account-already-initialized"]}'


def test_create_account():
    message = '{"account": {"active-card": true, "available-limit": 100}}'
    mng_acc.account_dict = {}
    creation_response = mng_acc.create_account(message, logging)
    assert creation_response == '{"account": {"active-card": true, "available-limit": 100}, "violations": []}'

    mng_acc.account_dict = json.loads('{"account": {"active-card": true, "available-limit": 100}, "violations": []}')
    creation_response = mng_acc.create_account(message, logging)
    assert creation_response == '{"account": {"active-card": true, "available-limit": 100}, "violations": ["account-already-initialized"]}'

    mng_acc.account_dict = json.loads('{"account": {"active-card": false, "available-limit": 100}, "violations": []}')
    creation_response = mng_acc.create_account(message, logging)
    assert creation_response == '{"account": {"active-card": true, "available-limit": 100}, "violations": []}'

    message = '{"account": {"active-card": false, "available-limit": 100}}'
    mng_acc.account_dict = json.loads('{"account": {"active-card": true, "available-limit": 100}, "violations": []}')
    creation_response = mng_acc.create_account(message, logging)
    assert creation_response == '{"account": {"active-card": false, "available-limit": 100}, "violations": []}'


def test_check_account_initialized():
    mng_acc.account_dict = json.loads('{"account": {"active-card": false, "available-limit": 100}, "violations": []}')
    status = mng_acc.check_account_initialized(logging)
    assert status == 'card-not-active'

    mng_acc.account_dict = {}
    status = mng_acc.check_account_initialized(logging)
    assert status == 'account-not-initialized'

    mng_acc.account_dict = json.loads('{"account": {"active-card": true, "available-limit": 100}, "violations": []}')
    status = mng_acc.check_account_initialized(logging)
    assert status == 'account-already-initialized'
