import sqlite3
from util import to_text

__CREATE_TABLE_SQL__ = """
CREATE TABLE IF NOT EXISTS TABLENAME
(id TEXT PRIMARY KEY NOT NULL ,
value TEXT NOT NULL );
"""

__GET_SQL__ = """
SELECT value FROM TABLENAME WHERE id=? LIMIT 1;
"""
__SET_SQL__ = """
INSERT OR REPLACE INTO TABLENAME (id, value) VALUES (?,?);
"""
__DEL_SQL__ = """
DELETE FROM TABLENAME WHERE id=?;
"""

class HomeworkHelper():
    def __init__(self, date_string, filename='.\data\hwk\hwk.sqlite3'):
        """
        传入的日期用以建立表格。此处需要注意，默认格式为
        20180409
        """

        self.db = sqlite3.connect(filename, check_same_thread=False)
        self.db.text_factory = str
        self.tbname="HWD"+date_string
        self.tb_sql_str=__CREATE_TABLE_SQL__.replace('TABLENAME',self.tbname)
        self.get_sql_str = __GET_SQL__.replace('TABLENAME',self.tbname)
        self.set_sql_str = __SET_SQL__.replace('TABLENAME',self.tbname)
        self.del_sql_str =__DEL_SQL__.replace('TABLENAME',self.tbname)
        self.db.execute(self.tb_sql_str)
    
    def get(self, id):
        """
        根据 id 获取数据。
        :param id: 要获取的数据的 id
        :return: 返回取到的数据，如果是空则返回一个空的 ``dict`` 对象
        """
        session_json = self.db.execute(
            self.get_sql_str, (id, )
        ).fetchone()
        if session_json is None:
            return ""
        return to_text(session_json[0])

    def set(self, id, value):
        """
        根据 id 写入数据。
        :param id: 要写入的 id
        :param value: 要写入的数据，可以是一个 ``dict`` 对象
        """
        self.db.execute(
            self.set_sql_str,
            (id, value)
        )
        self.db.commit()

    def delete(self, id):
        """
        根据 id 删除数据。
        :param id: 要删除的数据的 id
        """
        self.db.execute(self.del_sql_str, (id, ))
        self.db.commit()
        
    def checkunsubmit(self, ids):
        unsubmitlist=[]
        for id in ids:
            if(len(self.get(id))==0):
                unsubmitlist.append(id)
        return unsubmitlist
            
