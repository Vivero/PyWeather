import hashlib, json, os, re, requests, yaml

class WeatherUnderground:

    def __init__(self, city, state, auth_key):
        self.city = city
        self.state = state
        self.auth_key = auth_key
        self.wu_api_url = 'http://api.wunderground.com/api/{0}/conditions/q/{1}/{2}.json'

    def get_data(self):
        
        # http GET on Weather Underground API
        wu_response = requests.get(self.wu_api_url.format(self.auth_key, self.state, self.city))

        # check the response
        try:
            wu_response.raise_for_status()
        except Exception as e:
            print("WeatherUnderground.get_data exception: '{:s}'".format(str(e)))
            return None

        # return JSON-formatted data
        return wu_response.json()

