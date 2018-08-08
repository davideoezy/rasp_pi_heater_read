#!/usr/bin/python3
import mysql.connector as mariadb
import glob
import sys
import time

# ---------------- Initialise variables ------------------
# Device id
device = "RPi_1"
# Server db connection
host_ip = '192.168.0.10'
host_port = '3308'
host_db_name = 'pi_test'
host_uid = 'pi'
host_pword = 'raspberry'


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
        time.sleep(10)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

#Connect to mariadb

while True:
    con = mariadb.connect(host=host_ip, port=host_port, user=host_uid, password=host_pword, database=host_db_name)
    cur = con.cursor()
    try:
        cur.execute("""INSERT INTO temperature (device,temp) VALUES ('{}',{})""".format(device,read_temp()))
        con.commit()
    except:
        con.rollback()
    con.close()
