"""
This is a class where all the business logic is written to handle account management
"""
from pyscripts.util import message_utils


class ManageAccount:

    # initializing the class
    def __init__(self):
        self.account_dict = {}

    # Method to update the account with the violations raised
    def generate_violations(self, violations_list, logging, json_data):

        response_dict = ""
        if len(self.account_dict) > 1:
            logging.info(f"violations when account dict is not empty:{violations_list}")
            if len(violations_list) > 0:
                if len(self.account_dict['violations']) > 0:
                    self.account_dict.update(
                        violations=((self.account_dict['violations']) + violations_list))
                else:
                    self.account_dict.update(violations=violations_list)
            else:
                if len(json_data) > 0:
                    self.account_dict.update(account=json_data['account'])
                self.account_dict.update(violations=[])
            response_dict = message_utils.convert_to_string_to_json(self.account_dict, "JSON")
        else:
            logging.info(f"violations when account dict is empty:{violations_list}")
            if len(json_data) == 0:
                json_data = {"account": None, "violations": violations_list}
            else:
                logging.info(f"in else violations:{json_data}")
                json_data.update(violations=[])
                self.account_dict.update(json_data)
            response_dict = message_utils.convert_to_string_to_json(json_data, "JSON")

        logging.info(f" account dict after violations : {response_dict}")
        return response_dict

    # Method to create the account if not created or change the card active state from inactive to active and vice-versa
    def create_account(self, message, logging):
        logging.info(f"incoming account details: {message}")
        json_data = message_utils.convert_to_string_to_json(message, "STRING")
        account_status = self.check_account_initialized(logging)
        logging.info(f"account status:{account_status}")
        if account_status == "account-already-initialized":
            if json_data['account']['active-card'] != self.account_dict['account']['active-card']:
                return self.generate_violations([], logging, json_data)
            return self.generate_violations(["account-already-initialized"], logging, json_data)
        elif account_status == "account-not-initialized" or account_status == "card-not-active":
            return self.generate_violations([], logging, json_data)

    # Method to check whether the account is initialized and return the status of account
    def check_account_initialized(self, logging):
        if len(self.account_dict) == 0 or (len(self.account_dict) > 0 and self.account_dict['account'] is None):
            logging.info(" not initialized")
            return "account-not-initialized"
        elif len(self.account_dict) > 0 and self.account_dict['account'] is not None and self.account_dict['account'][
            'active-card'] and self.account_dict['account']['available-limit'] > 0:
            logging.info(" already initialized")
            return "account-already-initialized"
        elif len(self.account_dict) > 0 and self.account_dict['account'] is not None and not \
        self.account_dict['account'][
            'active-card']:
            logging.info("card not active")
            return "card-not-active"
