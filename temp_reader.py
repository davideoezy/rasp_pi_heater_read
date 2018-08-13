#!/usr/bin/python3
# Need mysql.connector - sudo apt-get -y install python3-mysql.connector

import mysql.connector as mariadb
import glob
import sys
import time
import io

# ---------------- Initialise variables ------------------
# Device id
device = "RPi_2"

# Initialise db parameters in connection string below

#Conect to sensor
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# Read device info
def read_rom():
    name_file=device_folder+'/name'
    f = open(name_file,'r')
    return f.readline()

#Raw temp
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(30)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

# Read CPU temp
f = open("/sys/class/thermal/thermal_zone0/temp", "r")
cpu_temp_string = (f.readline ())
cpu_temp = float(temp_cpu_string) / 1000.0

#Connect to mariadb

while True:
    con = mariadb.connect(host='192.168.0.10', port='3306', user='user', password='password', database='db')
    cur = con.cursor()
    try:
        cur.execute("""INSERT INTO temperature (device,temp, cpu_temp) VALUES ('{}',{},{})""".format(device,read_temp(),cpu_temp))
        con.commit()
    except:
        con.rollback()
    con.close()
#    print("""INSERT INTO temperature (device,temp) VALUES ('{}',{})""".format(device,read_temp()))
    time.sleep(30)
