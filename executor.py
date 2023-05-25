from account import Account
from action import Action, PostAction, RTAction, SRTAction
from post import Post
from typing import List
from dotenv import load_dotenv
import tweepy
import os
import telegram
import asyncio

load_dotenv()

CUSTOMER_API_KEY = os.getenv("CUSTOMER_API_KEY")
CUSTOMER_API_KEY_SECRET = os.getenv("CUSTOMER_API_KEY_SECRET")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")


class ExecutorInterface:
    def post(self, account: Account, post: Post) -> int:
        """Post tweet from account"""
        pass

    def rt(self, account: Account, tweet_id: int, tweet_url: str, uuid: str, srt: bool = False):
        """Retweet tweet from account"""
        pass

    def srt(self, account: Account, tweet_id: int, tweet_url: str, uuid: str):
        """Retweet tweet from account"""
        pass

    def post_tg(self, text: str, bot_token: str, chat_id: str):
        bot = telegram.Bot(bot_token)
        asyncio.ensure_future(bot.send_message(text=text, chat_id=chat_id))


class Executor(ExecutorInterface):

    rt_work_around_mode: bool = True

    def post(self, account: Account, post: Post) -> int:
        print("Posting", account.name, post.id, post.text, post.img_path)
        client = tweepy.Client(account.bearer_token)
        print(f"Account {account.name} {account.bearer_token}")
        media_ids = None
        if post.img_path is not None:
            auth = tweepy.OAuth1UserHandler(
                CUSTOMER_API_KEY,
                CUSTOMER_API_KEY_SECRET,
                account.access_token,
                account.access_token_secret
            )
            api = tweepy.API(auth)
            media = api.media_upload(filename=post.img_path)
            media_ids = [media.media_id]
        result = client.create_tweet(text=post.text, media_ids=media_ids, user_auth=False)
        print(result)
        return result.data["id"]

    def rt(self, account: Account, tweet_id: int, tweet_url: str, uuid: str, srt: bool = False):
        print("Self RTing" if srt else "RTing", account.name, tweet_id, uuid)
        print(f"Account {account.name} {account.bearer_token}")
        client = tweepy.Client(account.bearer_token)
        if self.rt_work_around_mode:
            result = client.create_tweet(text=tweet_url, user_auth=False)
            print(result)
        else:
            result = client.retweet(tweet_id, user_auth=False)
            print(result)
            result = client.like(tweet_id, user_auth=False)
            print(result)

    def srt(self, account: Account, tweet_id: int, tweet_url: str, uuid: str):
        self.rt(account, tweet_id, tweet_url, uuid)


class MockExecutor(ExecutorInterface):

    def post(self, account: Account, post: Post) -> int:
        print("Posting", account.name, post.id, post.text)
        return post.uuid()

    def rt(self, account: Account, tweet_id: int, tweet_url: str, uuid: str, srt: bool = False):
        print("RTing", account.name, tweet_id, uuid)

    def srt(self, account: Account, tweet_id: int, tweet_url: str, uuid: str):
        print("Self RTing", account.name, tweet_id, uuid)

    def post_tg(self, text: str, bot_token: str, chat_id: str):
        print("Posting to tg", text)


def update_actions_twee_id(actions: List[Action], tweet_id: int, tweet_url:str, uuid: str) -> List[Action]:
    for action in actions:
        if uuid == action.uuid and not isinstance(action, PostAction):
            action.tweet_id = tweet_id
            action.tweet_url = tweet_url
    return actions

def post_tg_if_soc(exexutor: ExecutorInterface, account: Account, text: str):
    if account.name == "sonsofcryptolabs":
        print("tg posting: ", text)
        exexutor.post_tg(text, TG_BOT_TOKEN, "-1001481837102")

def exec_next_action(executor: ExecutorInterface, actions: List[Action]) -> List[Action]:
    _actions = actions
    if len(_actions) <= 0:
        return _actions

    action = _actions.pop(0)

    if isinstance(action, PostAction):
        tweet_id = executor.post(action.account, action.post)
        tweet_url = f"https://twitter.com/{action.account.name}/status/{tweet_id}"
        _actions = update_actions_twee_id(_actions, tweet_id, tweet_url, action.uuid)
        post_tg_if_soc(executor, action.account, tweet_url)
    elif isinstance(action, RTAction):
        executor.rt(action.account, action.tweet_id, action.tweet_url, action.uuid)
        post_tg_if_soc(executor, action.account, action.tweet_url)
    elif isinstance(action, SRTAction):
        executor.srt(action.account, action.tweet_id, action.tweet_url, action.uuid)
        post_tg_if_soc(executor, action.account, action.tweet_url)
    else:
        print("Unexpected object type", action)

    return _actions
