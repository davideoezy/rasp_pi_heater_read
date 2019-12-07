#!/usr/bin/python3
import mysql.connector as mariadb
import datetime
import time

#Conectamos a la DB
con = mariadb.connect(host='192.168.0.10', port='3306', user='pi', password='raspberry', database='pi_test')

cur = con.cursor()

test_string = "test message 7"

ts = time.time()
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

try:
        cur.execute("""INSERT INTO message2 (text) VALUES ('{}')""".format(test_string))
        con.commit()
except:
        con.rollback()

con.close()

print("""INSERT INTO message2 (text,ts) VALUES ('{}')""".format(test_string))


