"""
This is a class where all the business logic is written to handle account initialization and transaction authorization
"""
from pyscripts.constants.app_constants import MAX_TRANSACTION_THRESHOLD, SIMILAR_TRANSACTION_THRESHOLD
from pyscripts.util import message_utils


class AuthorizeTransaction:

    # initializing the class with dictionaries
    def __init__(self):
        self.transaction_dict = {}
        self.violated_transaction_dict = {}

    # Method to check the transaction acceptance in a two minute slot
    def check_txn_acceptance_in_time_slot(self, transaction_json_data, logging):
        transaction_time_key_str = message_utils.get_transaction_time_key(transaction_json_data)
        logging.info(
            f" the transaction_time_key : {transaction_time_key_str} for transaction request :{transaction_json_data}")
        logging.info(f"the transaction dict:{self.transaction_dict}")
        if len(self.transaction_dict) > 0:
            if transaction_time_key_str in self.transaction_dict:
                transaction_no = len(self.transaction_dict[transaction_time_key_str])
                logging.info(f"Number of transactions for a transaction_time_key : {transaction_no}")
                if transaction_no < MAX_TRANSACTION_THRESHOLD:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return True

    # Method to check whether a similar transaction has been authorized already or not
    def check_similar_txn_already_in_time_slot(self, transaction_json_data, logging):
        transaction_time_key_str = message_utils.get_transaction_time_key(transaction_json_data)
        logging.info(
            f" the transaction_time_key : {transaction_time_key_str} for transaction request :{transaction_json_data}")
        similar_txn_count = 0
        logging.info(f"the transaction dict:{self.transaction_dict}")
        if len(self.transaction_dict) > 0:
            logging.info(f" the transaction_dict : {self.transaction_dict}")
            if transaction_time_key_str in self.transaction_dict:
                for key in self.transaction_dict[transaction_time_key_str]:
                    logging.info(
                        f" similar transactions for the transaction key : {self.transaction_dict[transaction_time_key_str]}")
                    if self.transaction_dict[transaction_time_key_str][key]['transaction']['merchant'] == \
                            transaction_json_data['transaction'][
                                'merchant'] \
                            and self.transaction_dict[transaction_time_key_str][key]['transaction']['amount'] == \
                            transaction_json_data['transaction']['amount']:
                        similar_txn_count += 1
                if similar_txn_count == SIMILAR_TRANSACTION_THRESHOLD:
                    return True
                elif similar_txn_count < SIMILAR_TRANSACTION_THRESHOLD:
                    return False
            else:
                return False
        else:
            return False

    # Method to append the transaction details in transaction dict
    def append_transaction(self, txn_dict, txn_json_data, logging):
        transaction_time_key_str = message_utils.get_transaction_time_key(txn_json_data)
        if len(txn_dict) > 0 and transaction_time_key_str in txn_dict:
            transaction_no = len(txn_dict[transaction_time_key_str])
            transaction_no += 1
            txn_dict[transaction_time_key_str][transaction_no] = txn_json_data
        else:
            temp_dict = {1: txn_json_data}
            txn_dict[transaction_time_key_str] = temp_dict
        logging.info(f"txn dictionary after adding transactions:{txn_dict}")

    # Method to authorize the transaction based on the business rules given
    def process_transaction(self, message, account_svc_obj, logging):
        try:
            txn_json_data = message_utils.convert_to_string_to_json(message, "STRING")
            account_status = account_svc_obj.check_account_initialized(logging)
            logging.info(f"account dict during the transaction authorization:{account_svc_obj.account_dict}")
            logging.info(f"account status during the transaction authorization:{account_status}")
            logging.info(f"transaction_dict during the transaction authorization:{self.transaction_dict}")
            if account_status == "card-not-active":
                txn_json_data.update(violations=["card-not-active"])
                self.append_transaction(self.violated_transaction_dict, txn_json_data, logging)
                return account_svc_obj.generate_violations(["card-not-active"], logging, {})
            elif account_status == "account-already-initialized":
                available_limit = account_svc_obj.account_dict['account']['available-limit']
                transaction_amount = txn_json_data['transaction']['amount']
                if transaction_amount > available_limit:
                    txn_json_data.update(violations=["insufficient-limit"])
                    self.append_transaction(self.violated_transaction_dict, txn_json_data, logging)
                    return account_svc_obj.generate_violations(["insufficient-limit"], logging, {})
                else:
                    if self.check_txn_acceptance_in_time_slot(txn_json_data, logging):
                        if not self.check_similar_txn_already_in_time_slot(txn_json_data, logging):
                            available_amount_limit = {"available-limit": int(available_limit - transaction_amount)}
                            account_svc_obj.account_dict['account'].update(available_amount_limit)
                            if available_amount_limit == 0:
                                inactive_card = {"active-card": False}
                                account_svc_obj.account_dict['account'].update(inactive_card)
                            self.append_transaction(self.transaction_dict, txn_json_data, logging)
                            account_svc_obj.account_dict.update(violations=[])
                            return message_utils.convert_to_string_to_json(account_svc_obj.account_dict, "JSON")
                        else:
                            txn_json_data.update(violations=["doubled-transaction"])
                            self.append_transaction(self.violated_transaction_dict, txn_json_data, logging)
                            return account_svc_obj.generate_violations(["doubled-transaction"], logging, {})
                    else:
                        txn_json_data.update(violations=["high-frequency-small-interval"])
                        self.append_transaction(self.violated_transaction_dict, txn_json_data, logging)
                        return account_svc_obj.generate_violations(["high-frequency-small-interval"], logging, {})
            else:
                txn_json_data.update(violations=["account-not-initialized"])
                self.append_transaction(self.violated_transaction_dict, txn_json_data, logging)
                return account_svc_obj.generate_violations(["account-not-initialized"], logging, {})
        except Exception as e:
            logging.error(e)
