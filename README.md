rasp_pi_heater_read

Python3 script to read the temperature from a DS18B20. These temperature readings will be inserted to a SQL database running on another network node.

Instructions - Common:
1. Ensure 1-wire is enabled on Raspbery Pi (Zero running Raspbian Pi in my case)
2. Install mqtt - sudo apt-get -y install python3-paho-mqtt
3. Create git folder in home directory on Pi
4. Clone repo

Instructions - Pi temp logger
5. Edit temp_reader.py to set device ID
6. cp pi_temp_reader.service /etc/systemd/system/
7. Enable pi_temp_reader.service

All things working, you should expect to see temperature entries published every 10 seconds
