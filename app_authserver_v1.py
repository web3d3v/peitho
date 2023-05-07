from dotenv import load_dotenv
from OpenSSL import SSL
from flask import Flask, redirect, session, request
from datetime import datetime
from OpenSSL import crypto
import os
import tweepy
from urllib.parse import urlparse
from urllib.parse import parse_qs

load_dotenv()

CUSTOMER_API_KEY = os.getenv("CUSTOMER_API_KEY")
CUSTOMER_API_KEY_SECRET = os.getenv("CUSTOMER_API_KEY_SECRET")
AUTH_BEARER_TOKEN = os.getenv("AUTH_BEARER_TOKEN")
WEB3_DEV_ACCESS_TOKEN = os.getenv("WEB3_DEV_ACCESS_TOKEN")
WEB3_DEV_ACCESS_TOKEN_SECRET = os.getenv("WEB3_DEV_ACCESS_TOKEN_SECRET")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

oauth1_user_handler = tweepy.OAuth1UserHandler(
    consumer_key=CUSTOMER_API_KEY,
    consumer_secret=CUSTOMER_API_KEY_SECRET,
    callback="https://localhost:5000/callback"
)

url = oauth1_user_handler.get_authorization_url()
print(url)

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'  # Needed for sessions in flask


# Visiting localhost:5000 will redirect to Twitter's app authorization page
@app.route("/")
def home():
    session['request_token'] = app.secret_key
    return redirect(url)


# If approved you'll be redirected back to localhost:5000/callback, printing the key and secret to the screen
@app.route("/callback")
def callback_for_app():
    print("[REQUEST]", request)
    print("[REQUEST URL]", request.url)
    parsed_url = urlparse(request.url)
    oauth_token = parse_qs(parsed_url.query)['oauth_token'][0]
    oauth_verifier = parse_qs(parsed_url.query)['oauth_verifier'][0]
    access_token, access_token_secret = oauth1_user_handler.get_access_token(
        oauth_verifier
    )
    msg = "\n" + \
          f"[oauth_token] {oauth_token} \n" + \
          f"[oauth_verifier] {oauth_verifier} \n" + \
          f"[access_token] {access_token} \n" + \
          f"[access_token_secret] {access_token_secret} \n"
    print(msg)
    return msg


if __name__ == "__main__":
    app.run(ssl_context="adhoc", debug=True)
