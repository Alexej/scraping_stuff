from os import listdir, supports_bytes_environ
from Helpers import dump_json
from os.path import isfile, join
import json

export_path = r"C:\Users\user\Desktop\python\scraper\exports"

exports = [join(export_path, file) for file in listdir(export_path) if isfile(join(export_path, file))]
json_exports = [json.load(open(export)) for export in exports]

urls = []

for export in json_exports:
    entries = export[0]["windows"]
    k = list(entries.keys())[0]
    for entrie in entries[k]:
        urls.append(entries[k][entrie]["url"])

f = open("urls.txt", "w+")

for url in urls:
    f.write("{}\n".format(url))


f.close()