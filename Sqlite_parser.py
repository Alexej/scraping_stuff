import sqlite3
import os
from typing import List


class Sqlite_parser:
    QUERY_FROM = "SELECT {} from {}"
    QUERY_FROM_LIKE = "SELECT {} from {} WHERE {}='{}'"

    def __init__(self, db_path, db_name) -> None:
        db_path = os.path.join(db_path, db_name)
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def select_from(self, name : str, table : str) -> List[str]:
        entries = self.cursor.execute(
            self.QUERY_FROM.format(name, table)).fetchall()
        return entries

    def select_from_like(self, name : str, table : str, where : str, equals : str) -> List[str]:
        entries = self.cursor.execute(self.QUERY_FROM_LIKE.format(
            name, table, where, equals)).fetchall()
        return entries

    def __dell__(self) -> None:
        self.connection.close()
