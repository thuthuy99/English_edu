#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql

def connection():
    # db = pymysql.connect(host, port, user, password, db_name)
    db = pymysql.connect(db='learning', user='root', passwd='', host='localhost', port=3307)
    return db


if __name__ == "__main__":
    cursor = connection().cursor()
    query = "SELECT * FROM doc1"
    cursor.execute(query)
    results = cursor.fetchall()
    for result in results:
        print(result[1])

