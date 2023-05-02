from dotenv import load_dotenv
from OpenSSL import SSL
from flask import Flask, redirect, session, request
from datetime import datetime
from OpenSSL import crypto
import os
import tweepy

load_dotenv()

CUSTOMER_API_KEY = os.getenv("CUSTOMER_API_KEY")
CUSTOMER_API_KEY_SECRET = os.getenv("CUSTOMER_API_KEY_SECRET")
AUTH_BEARER_TOKEN = os.getenv("AUTH_BEARER_TOKEN")
WEB3_DEV_ACCESS_TOKEN = os.getenv("WEB3_DEV_ACCESS_TOKEN")
WEB3_DEV_ACCESS_TOKEN_SECRET = os.getenv("WEB3_DEV_ACCESS_TOKEN_SECRET")
CLIENT_ID=os.getenv("CLIENT_ID")
CLIENT_SECRET=os.getenv("CLIENT_SECRET")

oauth2_user_handler = tweepy.OAuth2UserHandler(
    client_id=CLIENT_ID,
    redirect_uri="https://localhost:5000/callback",
    scope=["follows.read", "users.read", "tweet.read", "offline.access", "tweet.write", "like.write"],
    client_secret=CLIENT_SECRET,
)

url = oauth2_user_handler.get_authorization_url()
print(url)

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT' # Needed for sessions in flask

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
    access_token = oauth2_user_handler.fetch_token(request.url)
    print("[ACCESS_TOKEN]", access_token)
    user_client = tweepy.Client(access_token["access_token"])
    me = user_client.get_me(user_auth=False)
    print(me)
    result = user_client.create_tweet(text="Hello world {}".format(datetime.now()), user_auth=False)
    print(result)
    return "{}<br/>{}<br/>{}".format(access_token, me, result)

if __name__=="__main__":
    app.run(ssl_context="adhoc", debug=True)
