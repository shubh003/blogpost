import MySQLdb
from itertools import izip

import settings

MYSQL_HOST = settings.MYSQL_HOST
MYSQL_USER = settings.MYSQL_USER
MYSQL_DB = settings.MYSQL_DB
MYSQL_PASSWORD = settings.MYSQL_PASSWORD

class MySQL(object):

    def __init__(self, host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, db=MYSQL_DB):
        self.conn = None
        self.host = host
        self.user = user
        self.password = password
        self.db = db

        self.connect()

    def connect(self):
        self.conn = MySQLdb.connect(self.host, self.user, self.password, self.db)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        self.conn.close()

    def _get_query_result_as_list(self, query):
        """
        Fetches all results from given query as a list
        """
        if not self.execute_query(query):
            return []

        columns = [d[0].lower() for d in self.cursor.description]
        all_results = self.cursor.fetchall()

        l = []
        for placeholders in all_results:
            l.append(dict(izip(columns, placeholders)))

        return l

    def execute_query(self, query):
        try:
            return self.cursor.execute(query)
        except MySQLdb.OperationalError:
            self.connect()
            return self.cursor.execute(query)