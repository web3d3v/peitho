import jsonpickle
import post
from account import Account
from typing import List
from post import Post
from utils import read_from_file, write_to_file

ACTIONS_PATH = ".run/actions.json"


class Action:
    uuid: str
    account: Account


class PostAction(Action):
    post: Post

    def __init__(self, account: Account, post: Post):
        self.uuid = post.uuid()
        self.account = account
        self.post = post


class RTAction(Action):
    tweet_id: int = None

    def __init__(self, account: Account, post: Post):
        self.uuid = post.uuid()
        self.account = account


class SRTAction(Action):
    tweet_id: int = None

    def __init__(self, account: Account, post: Post):
        self.uuid = post.uuid()
        self.account = account


def generate_actions(account_a: Account, account_b: Account) -> List[Action]:
    cpa_posts = post.cpa_posts()
    mem_posts = post.mem_posts()
    jka_posts = post.jka_posts()
    cpb_posts = post.cpb_posts()
    fre_posts = post.fre_posts()
    jkb_posts = post.jkb_posts()
    actions: List = []
    for i in range(0, 30):
        actions.append(PostAction(account_a, cpa_posts[i]))
        actions.append(PostAction(account_b, mem_posts[i]))
        actions.append(PostAction(account_a, jka_posts[i]))
        actions.append(PostAction(account_b, cpb_posts[i]))
        actions.append(PostAction(account_a, fre_posts[i]))
        actions.append(PostAction(account_b, jkb_posts[i]))
        actions.append(RTAction(account_a, mem_posts[i]))
        actions.append(RTAction(account_b, cpa_posts[i]))
        actions.append(RTAction(account_a, cpb_posts[i]))
        actions.append(RTAction(account_b, jka_posts[i]))
        actions.append(RTAction(account_a, jkb_posts[i]))
        actions.append(RTAction(account_b, fre_posts[i]))
        actions.append(SRTAction(account_a, cpa_posts[i]))
        actions.append(SRTAction(account_b, mem_posts[i]))
        actions.append(SRTAction(account_a, jka_posts[i]))
        actions.append(SRTAction(account_b, cpb_posts[i]))
        actions.append(SRTAction(account_a, fre_posts[i]))
        actions.append(SRTAction(account_b, jkb_posts[i]))
    return actions


def load_actions(account_a: Account, account_b: Account) -> List[Action]:
    # restore or generate actions if needed
    actions_data = read_from_file(ACTIONS_PATH)
    if actions_data is not None:
        actions = jsonpickle.decode(actions_data)
    else:
        actions = generate_actions(account_a, account_b)
        store_actions(actions)
    return actions


def store_actions(actions: List[Action]):
    write_to_file(jsonpickle.encode(actions), ACTIONS_PATH)
