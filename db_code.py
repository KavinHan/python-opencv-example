#!/usr/bin/env python3
# encoding: utf-8

"""
@version: 3.7
@author: kavin
@file: db_code.py
@time: 2019-08-19 10:38
"""

import sys
import pymysql


class Database:
    """Database connection class."""

    def __init__(self, config):
        self.host = config['db_host']
        self.username = config['db_user']
        self.password = config['db_password']
        self.port = config['db_port']
        self.dbname = config['db_name']
        self.conn = None

    def open_connection(self):
        """Connect to MySQL Database."""
        try:
            if self.conn is None:
                self.conn = pymysql.connect(self.host,
                                            user=self.username,
                                            passwd=self.password,
                                            db=self.dbname,
                                            connect_timeout=5)
        except pymysql.MySQLError as e:
            print(e)
        finally:
            print('Connection opened successfully.')

    def run_query(self, query):
        """Execute SQL query."""
        try:
            self.open_connection()
            with self.conn.cursor() as cur:
                print('mysql run query: ' + query)
                if 'SELECT' in query:
                    records = []
                    cur.execute(query)
                    result = cur.fetchall()
                    for row in result:
                        records.append(row)
                    cur.close()
                    return records
                else:
                    cur.execute(query)
                    self.conn.commit()
                    affected = f"{cur.rowcount} rows affected."
                    cur.close()
                    return affected
        except pymysql.MySQLError as e:
            print(e)
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None
                print('Database connection closed.')


# debug code
if __name__ == "__main__":
    # run for any ip address
    db = Database({
        'db_host': '127.0.0.1',
        'db_user': 'root',
        'db_password': 'dongdong',
        'db_port': 3306,
        'db_name': 'mysql-example'
    })
    sql = "INSERT INTO `image` (`original_url`, `result_url`) VALUES ('{!s}', '{!s}')".format('test.jpg', 'test.jpg')
    print(sql)
    db.run_query(sql)
    print(db.run_query('SELECT * from `image`'))
