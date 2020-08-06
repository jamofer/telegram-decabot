import json
import os
from dataclasses import dataclass
from datetime import time, datetime
from typing import List

from geopy.distance import geodesic


STORES_JSON_FILE = f'{os.path.dirname(__file__)}/stores.json'
STORES_JSON_WEEK_DAY_OFFSET = 1


@dataclass
class OpeningHour:
    week_day: int
    start: time
    end: time
    timezone: str


@dataclass
class GeoPosition:
    latitude: float
    longitude: float

    @property
    def coordinates(self):
        return self.latitude, self.longitude


@dataclass
class Store:
    id: str
    name: str
    phone: str
    url: str
    city: str
    zip_code: str
    address: str
    opening_hours: List[OpeningHour]
    position: GeoPosition

    @property
    def is_open(self):
        return any(_is_in_opening_hour(opening_hour) for opening_hour in self.opening_hours)


def _is_in_opening_hour(opening_hour):
    now = datetime.now()

    if opening_hour.week_day != now.weekday():
        return False

    return opening_hour.start <= now.time() <= opening_hour.end


class Stores(object):
    def __init__(self, json_filename=STORES_JSON_FILE):
        self.stores = []

        with open(json_filename) as stores_json_file:
            stores_json = stores_json_file.read()

        stores_dict = json.loads(stores_json)
        for store_dict in stores_dict:
            store = _decode_store(store_dict)
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


def _decode_store(store_dict):
    return Store(
        store_dict['store_id'],
        store_dict['name'],
        store_dict['contact']['phone'],
        store_dict['contact']['website'],
        store_dict['address']['city'],
        store_dict['address']['zipcode'],
        _address_from_store_dict(store_dict),
        _opening_hours_from_store_dict(store_dict),
        GeoPosition(store_dict['position'][1], store_dict['position'][0]),
    )


def _address_from_store_dict(store_dict):
    return '\n'.join(
        line for line in store_dict['address']['lines']
        if line is not None
    )


def _opening_hours_from_store_dict(store_dict):
    opening_hours = []
    usual_schedule = store_dict['opening_hours']['usual']
    timezone = store_dict['opening_hours']['timezone']

    for week_day, hours_opened in usual_schedule.items():
        opening_hours.extend(
            _decode_opening_hour(week_day, hour_opened, timezone)
            for hour_opened in hours_opened
        )

    return opening_hours


def _decode_opening_hour(week_day, hour_opened_dict, timezone):
    return OpeningHour(
        int(week_day) - STORES_JSON_WEEK_DAY_OFFSET,
        time.fromisoformat(hour_opened_dict['start']),
        time.fromisoformat(hour_opened_dict['end']),
        timezone
    )
