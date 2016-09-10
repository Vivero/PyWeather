import hashlib, json, os, re, requests, yaml

class WeatherUnderground:

    def __init__(self, city, state, auth_key):
        self.city = city
        self.state = state
        self.auth_key = auth_key
        self.wu_api_url = 'http://api.wunderground.com/api/{0}/conditions/q/{1}/{2}.json'

    def get_data(self):

        wu_response_json = None
        
        try:
            # http GET on Weather Underground API
            wu_response = requests.get(self.wu_api_url.format(self.auth_key, self.state, self.city))

            # check the response
            wu_response.raise_for_status()

            # get JSON-formatted data
            wu_response_json = wu_response.json()
            
        except Exception as e:
            print("WeatherUnderground.get_data exception: '{:s}'".format(str(e)))
            print("Weather Underground response: {:s}".format(wu_response.text))
            wu_response_json = None

        return wu_response_json

