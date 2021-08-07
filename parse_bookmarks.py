from Sqlite_parser import Sqlite_parser
from typing import List


folder_path = r"C:\Users\user\AppData\Roaming\Mozilla\Firefox\Profiles\4d8w1xhw.default-release"
db_name = "places.sqlite"


def escape_special_characters(str : str) -> None:
    return str.replace("'", "''")


def get_urls() -> List[str]:
    urls = []
    sqlite = Sqlite_parser(folder_path, db_name)
    titles = sqlite.select_from("title", "moz_bookmarks")
    for title in titles:
        title_f = escape_special_characters(title[0])
        url = sqlite.select_from_like("url", "moz_places", "title", title_f)
        if len(url) != 0:
            urls.append(url[0][0])
    return urls


def extract_urls() -> List[str]:
    urls = get_urls()
    youtube = []

    for url in urls:
        if "youtube" in url and url not in youtube:
            youtube.append(url)



    print("Youtube: {}".format(len(youtube)))
    return youtube
