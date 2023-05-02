import os
from dotenv import load_dotenv
from account import Account, load_accounts, load_mock_accounts
from action import load_actions, store_actions
from executor import MockExecutor, Executor, exec_next_action

load_dotenv()

CUSTOMER_API_KEY = os.getenv("CUSTOMER_API_KEY")
CUSTOMER_API_KEY_SECRET = os.getenv("CUSTOMER_API_KEY_SECRET")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


def run():
    soc_account, dev_account = load_mock_accounts()
    actions = load_actions(soc_account, dev_account)
    executor = MockExecutor()
    actions = exec_next_action(executor, actions)
    store_actions(actions)

if __name__ == "__main__":
    run()
