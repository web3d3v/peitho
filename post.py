import hashlib
import numpy as np
from typing import List


class Post:
    id: int
    text: str
    img_path: str

    def __init__(self, id: int, text: str = None, img_path: str = None):
        self.id = id
        self.text = text
        self.img_path = img_path

    def uuid(self) -> str:
        digest = hashlib.sha256()
        digest.update(self.__str__().encode("utf-8"))
        return digest.hexdigest()

    def __str__(self):
        return "Post(id: {}, text: {}, img_path: {})" \
            .format(self.id, self.text, self.img_path)

    def __repr__(self):
        return "Post(id: {}, text: {}, img_path: {})" \
            .format(self.id, self.text, self.img_path)


# load lists
def cpa_posts() -> List[Post]:

    return list(map(lambda x: Post(x, "cpa_posts", None), list(np.arange(30))))


def mem_posts() -> List[Post]:
    return list(map(lambda x: Post(x, "mem_posts", None), list(np.arange(30))))


def jka_posts() -> List[Post]:
    return list(map(lambda x: Post(x, "jka_posts", None), list(np.arange(30))))


def cpb_posts() -> List[Post]:
    return list(map(lambda x: Post(x, "cpb_posts", None), list(np.arange(30))))


def fre_posts() -> List[Post]:
    return list(map(lambda x: Post(x, "fre_posts", None), list(np.arange(30))))


def jkb_posts() -> List[Post]:
    return list(map(lambda x: Post(x, "jkb_posts", None), list(np.arange(30))))
