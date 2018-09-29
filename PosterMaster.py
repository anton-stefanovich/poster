import sqlite3
import time

class PosterMaster:
    __TABLE_NAME__ = 'posted_records'

    __FIELD_ID__ = 'id'
    __FIELD_TS__ = 'timestamp'

    @staticmethod
    def get_twitter_token():
        return None

    @staticmethod
    def get_facebook_token():
        return None

    def __init__(self, db_filename='poster.db'):
        self.connection = sqlite3.connect(db_filename)

        if not self.is_table_exists(self.__TABLE_NAME__):
            self.create_table(self.__TABLE_NAME__)

    def __del__(self):
        self.connection.commit()
        self.connection.close()

    def __get_count(self, query):
        result = self.connection.execute(query)
        return result.fetchone()[0]

    def is_table_exists(self, table_name):
        query = "SELECT COUNT(*) FROM sqlite_master " \
                "WHERE type = 'table' AND name = '{table_name}'" \
                    .format(table_name=table_name)

        return self.__get_count(query) == 1

    def create_table(self, table_name):
        column_id_name = self.__FIELD_ID__
        column_id_type = 'TEXT'
        column_id_key = 'PRIMARY KEY'

        column_ts_name = self.__FIELD_TS__
        column_ts_type = 'REAL'
        column_ts_key = ''

        query = 'CREATE TABLE {tn} (' \
                '{id_name} {id_type} {id_key},' \
                '{ts_name} {ts_type} {ts_key})'.format(tn=table_name,
            id_name=column_id_name, id_type=column_id_type, id_key=column_id_key,
            ts_name=column_ts_name, ts_type=column_ts_type, ts_key=column_ts_key)

        cursor = self.connection.cursor()
        cursor.execute(query)

    def insert_record(self, id):
        query = "INSERT INTO {tn} ({field_id}, {field_ts}) VALUES ('{id}', {ts})".format(
            tn=self.__TABLE_NAME__, field_id=self.__FIELD_ID__, field_ts=self.__FIELD_TS__,
            id=id, ts=time.time())

        cursor = self.connection.cursor()
        cursor.execute(query)

    def is_record_exists(self, id):
        query = "SELECT COUNT(*) FROM {table_name} " \
                "WHERE {field_id} = '{value_id}'".format(
                    table_name=self.__TABLE_NAME__,
                    field_id=self.__FIELD_ID__,
                    value_id=id)

        return self.__get_count(query) > 0

