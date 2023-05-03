import hashlib
import os
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
    return load_posts("cpa")


def mem_posts() -> List[Post]:
    return load_posts("mem")


def jka_posts() -> List[Post]:
    return load_posts("jka")


def cpb_posts() -> List[Post]:
    return load_posts("cpb")


def fre_posts() -> List[Post]:
    return load_posts("fre")


def jkb_posts() -> List[Post]:
    return load_posts("jkb")


def image_path(id: str, path: str) -> str:
    paths = os.listdir(path)
    if f"{id}.png" in paths:
        return f"{path}/{id}.png"
    if f"{id}.jpg" in paths:
        return f"{path}/{id}.jpg"
    if f"{id}.jpeg" in paths:
        return f"{path}/{id}.jpeg"
    return None


def post_from(id: str, text: str, path: str) -> Post:
    return Post(
        int(id),
        text=text if len(text) > 0 else None,
        img_path=image_path(id, path)
    )


def load_posts(name: str) -> List[Post]:
    path = f"./content/{name}"
    posts: List[Post] = list()
    curr_text: str = ""
    curr_id: str = ""
    with open(path + "/text.txt", "r") as file:
        while True:
            line = file.readline()
            if not line:
                break
            if line[0:3] == "#ID":
                curr_id = line[3:].strip()
                curr_text = curr_text.strip()
                if len(curr_text) <= 280:
                    posts.append(post_from(curr_id, curr_text, path))
                else:
                    print("dropping", curr_id, len(curr_text))
                curr_text = ""
            else:
                curr_text += line
    return posts
