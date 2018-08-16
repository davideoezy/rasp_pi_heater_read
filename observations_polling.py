#!/usr/bin/env python

from twisted.internet import reactor
from twisted.python import log
import logging
import txbom.observations
import mysql.connector as mariadb


class MyObservationsClient(txbom.observations.Client):

    def observationsReceived(self, observations):
        '''
        This method receives observation updates as they are retrieved.
        '''
        if self.observations:
            if self.observations.current:
                air_temp = observations.current.air_temp
                apparent_t = observations.current.apparent_t
                cloud = observations.current.cloud
                cloud_oktas = observations.current.cloud_oktas
                dewpt = observations.current.dewpt
                gust_kmh = observations.current.gust_kmh
                press = observations.current.press
                rain_trace = observations.current.rain_trace
                rel_hum = observations.current.rel_hum
                vis_km = observations.current.vis_km
                wind_dir = observations.current.wind_dir
                wind_spd_kmh = observations.current.wind_spd_kmh

# Insert records to db
                con = mariadb.connect(host='192.168.0.10', port='3306', user='user', password='pass', database='db')
                cur = con.cursor()
                try:
                    cur.execute("""INSERT INTO outside_conditions (
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
                    wind_spd_kmh)
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
                    %s)"""
                    % (air_temp,
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
                    wind_spd_kmh))

                    con.commit()
                except:
                    con.rollback()
                con.close()
            else:
                print "No current observation"
        else:
            print "No observations"

logging.basicConfig(level=logging.DEBUG)

# Send any Twisted log messages to logging logger
_observer = log.PythonLoggingObserver()
_observer.start()

# Adelaide observations identifier
observation_url = "http://reg.bom.gov.au/fwo/IDV60901/IDV60901.94870.json"

client = MyObservationsClient(observation_url)

# strart the client's periodic observations update service.
reactor.callWhenRunning(client.start)
reactor.run()
