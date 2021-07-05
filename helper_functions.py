"""
This module contains some rep
"""

import sqlite3
import sys

def create_sqlite_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except:
        print("Error:", sys.exc_info()[0])

    return conn

def create_table(cur, create_table_sql):
    """ create a table from the create_table_sql statement
    :param cur: Defined cursor
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        cur.execute(create_table_sql)
    except:
        print("Error:", sys.exc_info()[0])

def drop_table(cur, table_to_drop):
    """ drop a table
    :param conn: Defined cursor
    :param table_to_drop: specify the table name you want to drop
    :return:
    """

    sql_drop_table = f"drop table {table_to_drop}"

    try:
        cur.execute(sql_drop_table)
    except:
        print("Error:", sys.exc_info()[0])

def print_tables_in_database(cur):
    try:
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print(cur.fetchall())
    except:
        print("Error:", sys.exc_info()[0])