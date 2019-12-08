#!/usr/bin/python3

import glob
import sys
import time
import io
import subprocess
import paho.mqtt.client as mqtt

# ---------------- Initialise variables ------------------

topic = "sensors/inside/temperature"
measurement = "temperature"
location = "inside"
device_label = 'living_room'
wifi_interface = "wlan0"

CurrentWIFI = 0
wifi_ssid = ""
IP = ""
temp_c = 0

# Broker details:
broker_address="192.168.0.10" 
client = mqtt.Client("Pi_1")
client.connect(broker_address)

#Connect to sensor
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
        time.sleep(30)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

# Read CPU temp
def read_cpu_temp():
    f = open("/sys/class/thermal/thermal_zone0/temp", "r")
    cpu_temp_string = (f.readline ())
    cpu_temp = float(cpu_temp_string) / 1000.0
    return(cpu_temp)

# read wifi info
def read_wifi_signal_strength():
    try:
        proc = subprocess.Popen(["iwconfig",wifi_interface],stdout=subprocess.PIPE, universal_newlines=True)
        out, err = proc.communicate()
    
        for line in out.split("\n"):
            if("Quality" in line):
                line = line.replace("Link Quality=","")
                quality = line.split()[0].split('/')
                WIFI = int(round(float(quality[0]) / float(quality[1]) * 100))
        for line in out.split("\n"):
            if("ESSID" in line):
                line = line.strip()
                parsed = line.split(':')
                wifi_ssid = parsed[1].strip('"')
        return(WIFI, wifi_ssid)
    except:
        return("ERROR!-iwconfig")
    

def read_device_address():
    try:
        proc = subprocess.Popen(["ifconfig",wifi_interface],stdout=subprocess.PIPE, universal_newlines=True)
        out, err = proc.communicate()
        device_address = ""
        for line in out.split("\n"):
            if("192.168" in line):
                strings = line.split(" ")
                device_address = strings[9]
                return(device_address)
    except:
        return("ERROR!-ifconfig")

#Broadcast message

while True:
    reading_influx = "%s,location=%s,device=%s inside_temp=%s,cpu_temp=%s,device_ssid=%s,device_address=%s,wifi_signal_strength=%s" % (
        measurement, location, device_label, read_temp(),read_cpu_temp(),read_wifi_signal_strength()[1], read_device_address(), read_wifi_signal_strength()[0])
    print(reading_influx)

    client.publish(topic,str(reading_influx))
    time.sleep(10)