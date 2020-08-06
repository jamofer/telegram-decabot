import json
import os

from decathlon import store_decoder
from geopy.distance import geodesic


STORES_JSON_FILE = f'{os.path.dirname(__file__)}/stores.json'


class DecathlonStores(object):
    def __init__(self, json_filename=STORES_JSON_FILE):
        self.stores = []

        with open(json_filename) as stores_json_file:
            stores_json = stores_json_file.read()

        stores_dict = json.loads(stores_json)
        for store_dict in stores_dict:
            store = store_decoder.decode(store_dict)
            self.stores.append(store)

    def find_by_name(self, name):
        return [store for store in self.stores if name in store.name]

    def find_by_zip_code(self, zip_code):
        return [store for store in self.stores if zip_code in store.zip_code]

    def find_by_city(self, city):
        return [store for store in self.stores if city in store.city]

    def find_by_distance(self, position, radius_in_kilometers):
        stores_in_range = []

        for store in self.stores:
            distance = geodesic(position.coordinates, store.position.coordinates).kilometers
            if distance <= radius_in_kilometers:
                stores_in_range.append(store)

        return stores_in_range
