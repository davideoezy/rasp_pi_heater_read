#!/usr/bin/python3
# Need mysql.connector - sudo apt-get -y install python3-mysql.connector

import mysql.connector as mariadb
import glob
import sys
import time
import io
import subprocess

# ---------------- Initialise variables ------------------

device_label = 'RPi_0'
wifi_interface = "wlan0"
db_host = 'hda.amahi.net'
db_host_port = '3306'
db_user = 'rpi'
db_pass = 'warm_me'
db = 'temp_logger'

CurrentWIFI = 0
wifi_ssid = ""
IP = ""
temp_c = 0

#Connect to sensor
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
cpu_temp = float(cpu_temp_string) / 1000.0

# read wifi info
try:
    proc = subprocess.Popen(["iwconfig",wifi_interface],stdout=subprocess.PIPE, universal_newlines=True)
    out, err = proc.communicate()
    
    for line in out.split("\n"):
        if("Quality" in line):
            line = line.replace("Link Quality=","")
            quality = line.split()[0].split('/')
            WIFI = int(round(float(quality[0]) / float(quality[1]) * 100))
            wifi_signal_strength = WIFI
    for line in out.split("\n"):
        if("ESSID" in line):
            line = line.strip()
            parsed = line.split(':')
            wifi_ssid = parsed[1].strip('"')
except:
    print("WIFI READOUT ERROR! - iwconfig")

try:
    proc = subprocess.Popen(["ifconfig",wifi_interface],stdout=subprocess.PIPE, universal_newlines=True)
    out, err = proc.communicate()
    IP = ""
    for line in out.split("\n"):
        if("192.168" in line):
            strings = line.split(" ")
            device_address = strings[9]
except:
    print("WIFI READOUT ERROR! - ifconfig")

#Connect to mariadb

insert_stmt = """
INSERT INTO temperature
(device, temp, cpu_temp, device_ssid, device_address, wifi_signal_strength)
VALUES
('{}',{},{},'{}','{}',{})""".format(device_label,read_temp(),cpu_temp, wifi_ssid, device_address, wifi_signal_strength)

while True:
    con = mariadb.connect(host = db_host, port = db_host_port, user = db_user, database = db)
    cur = con.cursor()
    try:
        cur.execute(insert_stmt)
        con.commit()
    except:
        con.rollback()
    con.close()
    time.sleep(30)
