rasp_pi_heater_read

Python3 script to read the temperature from a DS18B20. These temperature readings will be inserted to a SQL database running on another network node.

Instructions - Common:
1. Ensure 1-wire is enabled on Raspbery Pi (Zero running Raspbian Pi in my case)
2. Install myslq-connector - sudo apt-get -y install python3-mysql.connector
3. Create git folder in home directory on Pi
4. Clone repo
5. Create db on SQL server

Instructions - Pi temp logger
1. Create SQL table 'temperature' in db, with columns 'device varchar(15), temp float, ts timestamp'
6. Grant access to Pi userid on SQL table
6. Edit temp_reader.py to set device ID and set db parameters
7. cp pi_temp_reader.service /etc/systemd/system/
8. Enable pi_temp_reader.service

All things working, you should expect to see temperature entries to the db table every 30 seconds
