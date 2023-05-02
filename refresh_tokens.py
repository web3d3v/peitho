from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import logging
import os
import tweepy

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

CUSTOMER_API_KEY = os.getenv("CUSTOMER_API_KEY")
CUSTOMER_API_KEY_SECRET = os.getenv("CUSTOMER_API_KEY_SECRET")
AUTH_BEARER_TOKEN = os.getenv("AUTH_BEARER_TOKEN")
WEB3_DEV_ACCESS_TOKEN = os.getenv("WEB3_DEV_ACCESS_TOKEN")
WEB3_DEV_ACCESS_TOKEN_SECRET = os.getenv("WEB3_DEV_ACCESS_TOKEN_SECRET")
CLIENT_ID=os.getenv("CLIENT_ID")
CLIENT_SECRET=os.getenv("CLIENT_SECRET")
WEB_BEAST_TOKEN=os.getenv("WEB_BEAST_TOKEN")
WEB_DEV_TOKEN=os.getenv("WEB_DEV_TOKEN")
WEB_TOKEN=os.getenv("WEB_TOKEN")
WEB_REFRESH_TOKEN=os.getenv("WEB_REFRESH_TOKEN")
BEAST_TOKEN=os.getenv("BEAST_TOKEN")
BEAST_REFRESH_TOKEN=os.getenv("BEAST_REFRESH_TOKEN")


oauth2_user_handler = tweepy.OAuth2UserHandler(
    client_id=CLIENT_ID,
    redirect_uri="https://localhost:5000/callback",
    scope=["follows.read", "users.read", "tweet.read", "offline.access", "tweet.write", "like.write"],
    client_secret=CLIENT_SECRET,
)

result = oauth2_user_handler.refresh_token(
    token_url="https://api.twitter.com/2/oauth2/token",
    refresh_token=BEAST_REFRESH_TOKEN,
    auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
)

print(result)
