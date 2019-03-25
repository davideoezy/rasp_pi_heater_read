

import urllib.request
import json
import datetime
import time
import mysql.connector as mariadb

# Set variables

# BOM readings
url = 'http://reg.bom.gov.au/fwo/IDV60901/IDV60901.94870.json'

# DB details
db_host = '192.168.0.10'
db_host_port = '3306'
db_user = 'rpi'
db_pass = 'warm_me'
db = 'temp_logger'

def response(url):
    with urllib.request.urlopen(url) as response: 
        jsonString = response.read()
        jsonData = json.loads(jsonString.decode('utf-8'))
        current_reading = jsonData['observations']['data'][0]
    return(current_reading)

while True:
    
    locals().update(response(url))
    
    reading_ts = datetime.datetime.strptime(local_date_time_full, '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')

    insert_stmt = """
INSERT INTO outside_conditions (
air_temp,
apparent_t,
cloud,
cloud_oktas,
dewpt,
gust_kmh,
press,
rain_trace,
rel_hum,
vis_km,
wind_dir,
wind_spd_kmh,
reading_ts)
VALUES
(%s,
%s,
'%s',
%s,
%s,
%s,
%s,
%s,
%s,
%s,
'%s',
%s,
'%s')""" % (air_temp, 
            apparent_t,
            cloud, 
            cloud_oktas, 
            dewpt, 
            gust_kmh, 
            press, 
            rain_trace, 
            rel_hum, 
            vis_km, 
            wind_dir, 
            wind_spd_kmh, 
            reading_ts)

    
    con = mariadb.connect(host = db_host, port = db_host_port, user = db_user, password = db_pass, database = db)
    cur = con.cursor()

    try:
        cur.execute(insert_stmt)
        con.commit()
    except:
        con.rollback()

    con.close()
    time.sleep(600)

