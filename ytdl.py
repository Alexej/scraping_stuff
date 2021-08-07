import subprocess
from typing import List
import os
import time
from parse_bookmarks import extract_urls
import colorama
from colorama import Fore

def error_code_log(code : int) -> None:
    if code == 0:
        print(Fore.GREEN)
    else:
        print(Fore.RED)
    print("Return Code: {}".format(code))
    print(Fore.RESET)

def write_urls(urls : List[str], file_to_save : str) -> None:
    file = open(file_to_save, "w")
    for el in urls:
        file.write(el + "\n")
    file.close()


def read_urls(path_to_urls : str) -> List[str]:
    urls_file = open(path_to_urls, "r")
    urls_list = []
    for url in urls_file.readlines():
        urls_list.append(url.rstrip('\n'))
    urls_file.close()
    return urls_list


def ytdl_wrapper(url : str, path_to_save : str) -> int:
    output_path = '-o "{}/%(title)s.%(ext)s"'
    command = "{} {} {}".format('youtube-dl', url, output_path.format(path_to_save))
    process = subprocess.Popen(command, shell=True)
    process.wait()
    return process.returncode


def download(urls: List[str], path_to_save : str, num_of_down : int) -> List[str]:
    urls_downloaded = []
    for index, url in enumerate(urls):
        print("Downloading: {}/{}".format(index + 1, num_of_down))
        return_code = ytdl_wrapper(url, path_to_save)
        error_code_log(return_code)
        if return_code == 0:
            urls_downloaded.append(url)
        if index + 1 == num_of_down:
            break
    return urls_downloaded

    
def main(path_to_urls : str, path_to_save : str, num_of_down : int, bookmarks : bool) -> None:
    urls_list = None
    if bookmarks:
        urls_list = extract_urls()
    else:
        urls_list = read_urls(path_to_urls)
        os.rename(path_to_urls, "{} {}.txt".format(path_to_urls.split(".")[0], time.time()) )
    downloaded = download(urls_list, path_to_save, num_of_down)
    rem = set(urls_list).difference(set(downloaded))
    if rem:
        write_urls(rem, path_to_urls)


if __name__ == '__main__':
    colorama.init()
    main("urls.txt", "videos", 100, bookmarks=False)