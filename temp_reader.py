#!/usr/bin/python3
import mysql.connector as mariadb
import glob
import sys

#Conect to sensor
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

#Raw temp
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(10)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        #Not even the best solution, but seems the DS18B20 reads 3* upper than the real
        return temp_c - 3

device = "RPi_1"

#Connect to mariadb
con = mariadb.connect(host='192.168.0.10', port='3306', user='pi', password='raspberry', database='pi_test')
cur = con.cursor()

try:
        cur.execute("""INSERT INTO temperature (device,temp)
                    VALUES ('{}',{})""".format(test_string,read_temp()))
        con.commit()
except:
        con.rollback()

con.close()
