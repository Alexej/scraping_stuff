import re
import os
import json
from typing import List
import requests
from typing import Pattern
from datetime import datetime
from bs4 import BeautifulSoup
from Helpers import *
import argparse


class FchanDownloader:
    board: str = ""
    catalog_url: str = "https://boards.4chan.org/{}/catalog"
    board_thread_url: str = "https://boards.4chan.org/{}/thread"
    re_json_threads: Pattern[str] = re.compile(
        "var catalog = (.+);var style_group")
    re_image_url: Pattern[str] = re.compile('fileThumb" href="(.+?)" target=')

    def __init__(self, board: str = "sci") -> None:
        self.set_board(board)

    def set_board(self, board: str) -> None:
        self.board = board

    #hacky
    def parse_json_script(self) -> dict:
        page = requests.get(self.catalog_url.format(self.board))
        soup = BeautifulSoup(page.content, "html.parser")
        scripts = soup.findAll("script")
        scripts_strings = []
        for script in scripts:
            scripts_strings.append(str(script))

        threads = self.re_json_threads.search(
            max(scripts_strings, key=len)).group(1)
        return json.loads(threads)

    def scrap_media_urls(self, url: str) -> List[str]:
        thread_html = requests.get(url)
        thread_soup = BeautifulSoup(thread_html.content, "html.parser")
        urls = re.findall(self.re_image_url, str(thread_soup))
        return urls

    def parse_thread(self, thread_id: int, thread: dict) -> None:
        thread_datetime = datetime.fromtimestamp(thread["date"])
        sub_folder_name = ""
        if len(thread["sub"]) > 0:
            sub_folder_name = thread["sub"]
        elif len(thread["teaser"]) > 0:
            if len(thread["teaser"]) > 50:
                sub_folder_name = thread["teaser"][0:50]
            else:
                sub_folder_name = thread["teaser"]
        else:
            pass
        sub_folder_name += " " + str(thread_datetime)
        sub_folder_path = os.path.join(
            self.board, remove_illegal_characters(sub_folder_name))

        make_dirs(sub_folder_path)

        thread_url = "{}/{}".format(
            self.board_thread_url.format(self.board), thread_id)
        image_urls = self.scrap_media_urls(thread_url)

        print(thread_url)
        print("Parsing thread {}".format(thread["sub"]))
        download_images(image_urls, sub_folder_path)

    def parse_threads(self, max_: int, min_num_of_img_per_thread: int = 1) -> None:
        json_threads = self.parse_json_script()
        num_of_thr_srcaped = 0
        for thread_id in json_threads["threads"]:
            thread = json_threads["threads"][thread_id]
            num_thr_imgs = thread['i']
            if num_thr_imgs > min_num_of_img_per_thread:
                self.parse_thread(thread_id, thread)
                num_of_thr_srcaped += 1
            if max_ and num_of_thr_srcaped == max_:
                break


def main():
    parser = argparse.ArgumentParser(description='4chan downloader.')
    parser.add_argument('--max', '-m', type=int, dest='max',
                        help='Maximum number of threads', required=True)
    parser.add_argument('--board', '-b', type=str,
                        dest='board', help='Board name', required=True)

    args = parser.parse_args()
    ch = FchanDownloader(args.board)
    ch.parse_threads(max_=args.max)


if __name__ == '__main__':
    main()
