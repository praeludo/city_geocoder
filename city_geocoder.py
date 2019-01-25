import json
import base64
import sys
from time import sleep

import requests
import redis


class Place:
    def __init__(self, email, country, city=""):
        self.email = email
        self._country = country
        self._city = city
        self.id = base64.b64encode(str.encode(str(self)))

    def __repr__(self):
        return f'{{"city": "{self.city}", "state": "{self.state}", "country": "{self.country}"}}'

    @property
    def country(self):
        return self._country.lower()

    @property
    def city(self):
        try:
            city = self._city.split(',')[0].strip()
        except AttributeError:
            city = ''
        return city.lower()

    @property
    def state(self):
        try:
            state = self._city.split(',')[1].strip()
        except (AttributeError, IndexError):
            state = ''
        return state.lower()
    
    def retrieve_from_osm(self, facets=True, resp_format="json"):
        payload = {"limit": 1,
                  "email": self.email,
                   "format": resp_format}
        headers = {"user-agent": f"requests/{requests.__version__} (python/{sys.version.split()[0]})"}
        if not facets:
            payload['q'] = f"{self.city}, {self.state}, {self.country}"
        else:
            payload['city'] = self.city
            payload["country"] = self.country
            payload["state"] = self.state,
        place = requests.get("https://nominatim.openstreetmap.org/search/", 
                             params=payload,
                             headers= headers).content
        return place
    
    def retrieve_coordinates(self):
        sleep(1)
        place = json.loads(self.retrieve_from_osm())
        if not place:
            sleep(1)
            place = json.loads(self.retrieve_from_osm(False))
        try:
            coordinates = f"{float(place[0]['lat'])}, {float(place[0]['lon'])}"
        except IndexError:
            coordinates = ''
        return coordinates
    
    def get_or_cache_coordinates(self):
        r = redis.StrictRedis()
        coordinates = r.get(self.id)
        if not coordinates:
            r.set(self.id, self.retrieve_coordinates())
            coordinates = r.get(self.id)
        return coordinates.decode()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--email", help="Your mail address", required=True)
    parser.add_argument("--country", help="Country of the place you're looking for", required=True)
    parser.add_argument("--city", help="City you're looking for")

    args = vars(parser.parse_args())
    print(Place(args['email'], args['country'], args['city']).get_or_cache_coordinates())
