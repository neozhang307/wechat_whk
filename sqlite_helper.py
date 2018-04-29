import sqlite3
from util import to_text,get_text,json_loads,json_dumps

__CREATE_TABLE_SQL__ = """
CREATE TABLE IF NOT EXISTS USER_INFO
(id TEXT PRIMARY KEY NOT NULL ,
value TEXT NOT NULL );
"""


class SQLiteHelper():

    def __init__(self, filename='.\data\session.sqlite3'):
        self.db = sqlite3.connect(filename, check_same_thread=False)
        self.db.text_factory = str
        self.db.execute(__CREATE_TABLE_SQL__)

    def get(self, id):
        """
        根据 id 获取数据。
        :param id: 要获取的数据的 id
        :return: 返回取到的数据，如果是空则返回一个空的 ``dict`` 对象
        """
        session_json = self.db.execute(
            "SELECT value FROM USER_INFO WHERE id=? LIMIT 1;", (id, )
        ).fetchone()
        if session_json is None:
            return {}
        return json_loads(session_json[0])

    def set(self, id, value):
        """
        根据 id 写入数据。
        :param id: 要写入的 id
        :param value: 要写入的数据，可以是一个 ``dict`` 对象
        """
        self.db.execute(
            "INSERT OR REPLACE INTO USER_INFO (id, value) VALUES (?,?);",
            (id, json_dumps(value))
        )
        self.db.commit()

    def delete(self, id):
        """
        根据 id 删除数据。
        :param id: 要删除的数据的 id
        """
        self.db.execute("DELETE FROM USER_INFO WHERE id=?;", (id, ))
        self.db.commit()


