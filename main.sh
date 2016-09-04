#!/bin/bash -ex

export PYTHONUNBUFFERED=1

WEATHER_UNDERGROUND_KEY_FILE="data/weather_api.sh"

if [[ -e "$WEATHER_UNDERGROUND_KEY_FILE" ]]; then
	source $WEATHER_UNDERGROUND_KEY_FILE
else
	printf "Missing '$WEATHER_UNDERGROUND_KEY_FILE'\n"
	printf "Create the file with the following contents:\n\n"
	printf "  export WEATHER_UNDERGROUND_KEY=<Weather Underground API key>\n"
	printf "\nReplace <Weather Underground API key> with the value from your Weather Underground API.\n\n"
	exit 1
fi

export PYWEATHER_DB_NAME='pynest'
export PYWEATHER_DB_USER='pynest'
export PYWEATHER_DB_PASS='flats44'
export PYWEATHER_DB_HOST='localhost'

export WEATHER_LOCATION_STATE='MA'
export WEATHER_LOCATION_CITY='Chelsea'

exec /usr/bin/python /opt/PyWeather/pyweather.py
