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
7. Copy pi_temp_reader.service to /etc/systemd/system/
8. Enable pi_temp_reader.service

All things working, you should expect to see temperature entries to the db table every 30 seconds

Weather poller

Python 2 script using txBOM to read observations of local station. Values inserted into a SQL database
running on another network node

Instructions - weather polling
1. pip/conda install twisted, logging, txbom, mysql-connector
2. Create SQL table 'outside_conditions' in db, with columns:
air_temp float,
apparent_t float,
cloud varchar(40),
cloud_oktas int,
dewpt float,
gust_kmh int,
press float,
rain_trace float,
rel_hum int,
vis_km int,
wind_dir varchar(10),
wind_spd_kmh int,
ts timestamp
3. Copy outside_conditions.service to /etc/systemd/system/
4. enable outside_conditions.service

All things working, a record will be inserted every 30 minutes
