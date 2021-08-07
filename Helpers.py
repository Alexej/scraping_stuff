from typing import List
import os
import json
import requests


def remove_illegal_characters(folder_name: str) -> str:
    ill_chars: str = r"\/:|<>*?"
    for character in ill_chars:
        folder_name = folder_name.replace(character, " ")
    return folder_name


def dump_json(obj: dict) -> None:
    print(json.dumps(obj, indent=2))


def save_image(url: str, path: str, name: str) -> None:
    req = requests.get("http:" + url, allow_redirects=True)
    open(os.path.join(path, name), 'wb').write(req.content)


def make_dirs(folder_path: str) -> None:
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def download_images(urls: List[str], sub_folder_path: str) -> None:
    for i, image_url in enumerate(urls):
        print("Image: {}/{} Url: {}".format(i + 1, len(urls), image_url))
        save_image(image_url, sub_folder_path, image_url.split("/")[-1])
