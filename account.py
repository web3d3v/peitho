import os
import pathlib
import jsonpickle
import tweepy
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

from utils import read_from_file, write_to_file

load_dotenv()

CUSTOMER_API_KEY = os.getenv("CUSTOMER_API_KEY")
CUSTOMER_API_KEY_SECRET = os.getenv("CUSTOMER_API_KEY_SECRET")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


class Account:
    name: str
    bearer_token: str
    refresh_token: str
    access_token: str
    access_token_secret: str

    def __init__(self, name: str, bearer_token: str, refresh_token: str, access_token: str, access_token_secret: str):
        self.name = name
        self.bearer_token = bearer_token
        self.refresh_token = refresh_token
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    def __str__(self):
        return "Account(name: {})".format(self.name)

    def __repr__(self):
        return self.__str__()


PATH = pathlib.Path(__file__).parent.resolve()
ACCOUNTS_PATH = f"{PATH}/.run/accounts.json"
MOCK_ACCOUNTS_PATH = f"{PATH}/.run/mock_accounts.json"


def load_accounts() -> (Account, Account):
    # restore or generate actions if needed
    accounts_data = read_from_file(ACCOUNTS_PATH)
    if accounts_data is not None:
        accounts = jsonpickle.decode(accounts_data)
    else:
        accounts = [
            Account(
                "sonsofcryptolabs",
                os.getenv("SOC_BEARER_TOKEN"),
                os.getenv("SOC_REFRESH_TOKEN"),
                os.getenv("SOC_ACCESS_TOKEN"),
                os.getenv("SOC_ACCESS_TOKEN_SECRET"),
            ),
            Account(
                "web3dev",
                os.getenv("DEV_BEARER_TOKEN"),
                os.getenv("DEV_REFRESH_TOKEN"),
                os.getenv("DEV_ACCESS_TOKEN"),
                os.getenv("DEV_ACCESS_TOKEN_SECRET"),
            ),
        ]

    soc_account = accounts[0]
    dev_account = accounts[1]
    soc_account = refresh_token(soc_account)
    dev_account = refresh_token(dev_account)
    write_to_file(jsonpickle.encode(accounts), ACCOUNTS_PATH)
    return soc_account, dev_account


def load_mock_accounts() -> (Account, Account):
    # restore or generate actions if needed
    accounts_data = read_from_file(MOCK_ACCOUNTS_PATH)
    if accounts_data is not None:
        accounts = jsonpickle.decode(accounts_data)
    else:
        accounts = [
            Account(
                "0xWeb3Beast",
                os.getenv("BEAST_BEARER_TOKEN"),
                os.getenv("BEAST_REFRESH_TOKEN"),
                os.getenv("BEAST_ACCESS_TOKEN"),
                os.getenv("BEAST_ACCESS_TOKEN_SECRET"),
            ),
            Account(
                "cryptu5maximu5",
                os.getenv("MAXIMUS_BEARER_TOKEN"),
                os.getenv("MAXIMUS_REFRESH_TOKEN"),
                os.getenv("MAXIMUS_ACCESS_TOKEN"),
                os.getenv("MAXIMUS_ACCESS_TOKEN_SECRET"),
            ),
        ]

    soc_account = accounts[0]
    dev_account = accounts[1]
    soc_account = refresh_token(soc_account)
    dev_account = refresh_token(dev_account)
    write_to_file(jsonpickle.encode(accounts), MOCK_ACCOUNTS_PATH)
    return soc_account, dev_account


def refresh_token(account: Account):
    oauth2_user_handler = tweepy.OAuth2UserHandler(
        client_id=CLIENT_ID,
        redirect_uri="https://localhost:5000/callback",
        scope=["follows.read", "users.read", "tweet.read", "offline.access", "tweet.write", "like.write"],
        client_secret=CLIENT_SECRET,
    )

    result = oauth2_user_handler.refresh_token(
        token_url="https://api.twitter.com/2/oauth2/token",
        refresh_token=account.refresh_token,
        auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
    )
    print(result)
    account.bearer_token = result["access_token"]
    account.refresh_token = result["refresh_token"]
    return account
