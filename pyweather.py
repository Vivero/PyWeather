#!/usr/bin/python

import argparse, json, os, psycopg2, re, signal, sys, yaml

from lib.weather_underground import WeatherUnderground

from datetime import datetime
from time import sleep

class PyWeather:

    def __init__(self, city, state, auth_key, db_info=None):
        self.terminate = False
        signal.signal(signal.SIGTERM, self.stop)

        # create Weather Underground API object
        self.weather = WeatherUnderground(city, state, auth_key)

        # use database?
        self.db_conn = None
        if db_info is not None:
            try:
                self.db_conn = psycopg2.connect(database=db_info['dbname'], user=db_info['dbuser'], password=db_info['dbpass'], host=db_info['dbhost'])
            except psycopg2.Error as e:
                print("Unable to connect to database!\n{:s}".format(str(e)))
                self.db_conn = None


    def start(self):
        while (not self.terminate):
            #dt = datetime.now()
            #print("PyWeather! {:s}".format(dt.strftime("%A, %d. %B %Y %I:%M:%S%p")))

            # get Nest API data
            weather_data = self.weather.get_data()
            #print json.dumps(weather_data, indent=4, sort_keys=True)

            # store in database
            if (weather_data is not None) and (self.db_conn is not None):
                
                observation_data = weather_data["current_observation"]

                relative_humidity = re.match(r"([0-9]+)", observation_data["relative_humidity"]).group(1)

                cursor = self.db_conn.cursor()
                cursor.execute("INSERT INTO weather_observations (weather, temp_f, wind_mph, relative_humidity, pressure_mb, precip_1hr_in, feelslike_f, raw_data, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now(), now())", (
                            observation_data['weather'],
                            observation_data['temp_f'],
                            observation_data['wind_mph'],
                            relative_humidity,
                            observation_data['pressure_mb'],
                            observation_data['precip_1hr_in'],
                            observation_data['feelslike_f'],
                            json.dumps(weather_data),
                        )
                    )
                self.db_conn.commit()
                cursor.close()

            # wait till next polling period
            sleep(600.0)

        print("Terminating...")

    def stop(self, signum, frame):
        self.terminate = True


if __name__ == '__main__':
    
    # parse command-line arguments
    #===========================================================================
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-d", "--no-db", 
        help="Disables the use of a database store",
        action="store_true")
    args = arg_parser.parse_args()
    
    disable_database = args.no_db
    
    
    # start the application
    #===========================================================================
    
    # environment setup
    auth_key = os.environ['WEATHER_UNDERGROUND_KEY']
    city = os.environ['WEATHER_LOCATION_CITY']
    state = os.environ['WEATHER_LOCATION_STATE']

    # data logger service
    db_info = None
    if not disable_database:
        db_info = {
            'dbname': os.environ['PYWEATHER_DB_NAME'],
            'dbuser': os.environ['PYWEATHER_DB_USER'],
            'dbpass': os.environ['PYWEATHER_DB_PASS'],
            'dbhost': os.environ['PYWEATHER_DB_HOST'],
        }

    pyweather = PyWeather(city, state, auth_key, db_info)
    pyweather.start()
    
    sys.exit(0)
