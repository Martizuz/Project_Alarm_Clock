import sqlite3

class BaseData:
    def __init__(self):
        self.conn = sqlite3.connect("fridge_records.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS records (event TEXT, camera TEXT, timestamp TEXT)")
        self.conn.commit()