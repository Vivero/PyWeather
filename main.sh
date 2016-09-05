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

PYWEATHER_DB_INFO_FILE="data/db_info.sh"

export WEATHER_LOCATION_STATE='MA'
export WEATHER_LOCATION_CITY='Chelsea'

if [[ -e "$PYWEATHER_DB_INFO_FILE" ]]; then
    source $PYWEATHER_DB_INFO_FILE

    exec /usr/bin/python /opt/PyWeather/pyweather.py

else
    printf "Missing '$PYWEATHER_DB_INFO_FILE'\n"
    printf "Create the file with the following contents:\n\n"
    printf "  export PYWEATHER_DB_NAME=<PostgreSQL database name>\n"
    printf "  export PYWEATHER_DB_USER=<PostgreSQL user name>\n"
    printf "  export PYWEATHER_DB_PASS=<PostgreSQL user password>\n"
    printf "  export PYWEATHER_DB_HOST=<PostgreSQL hostname>\n"
    printf "\nReplace <...> with appropriate credentials to access your PostgreSQL database.\n\n"
    printf "Running PyWeather with database disabled ...\n"
    
    exec /usr/bin/python /opt/PyWeather/pyweather.py --no-db
fi
