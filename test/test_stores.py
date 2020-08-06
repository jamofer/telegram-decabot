import calendar
import json
import unittest
from datetime import time, datetime

from decathlon import decathlon_stores, store_decoder
from decathlon.store import OpeningHour, GeoPosition
from mock import patch


class TestStores(unittest.TestCase):
    def tearDown(self) -> None:
        patch.stopall()

    def test_it_decodes_a_store_from_json(self):
        store_dict = json.loads(TEST_STORE_JSON)

        store = store_decoder.decode(store_dict)

        assert store.id == '001'
        assert store.name == 'Test'
        assert store.phone == '999 100 100 100'
        assert store.url == 'http://website.com'
        assert store.city == 'Gotham'
        assert store.address == 'Desenganyo 21'
        assert store.opening_hours == [
            OpeningHour(calendar.MONDAY, time(hour=10, minute=0), time(hour=20, minute=0), 'Europe/Paris'),
            OpeningHour(calendar.TUESDAY, time(hour=10, minute=0), time(hour=20, minute=0), 'Europe/Paris'),
            OpeningHour(calendar.WEDNESDAY, time(hour=10, minute=0), time(hour=20, minute=0), 'Europe/Paris'),
            OpeningHour(calendar.FRIDAY, time(hour=10, minute=0), time(hour=20, minute=0), 'Europe/Paris'),
            OpeningHour(calendar.SATURDAY, time(hour=10, minute=0), time(hour=20, minute=0), 'Europe/Paris'),
            OpeningHour(calendar.SUNDAY, time(hour=11, minute=0), time(hour=19, minute=0), 'Europe/Paris'),
        ]
        assert store.position == GeoPosition(latitude=39.572838, longitude=2.642547)

    def test_it_decodes_all_stores(self):
        decathlon_stores.DecathlonStores()

    def test_it_finds_stores_by_name(self):
        stores_collection = decathlon_stores.DecathlonStores()

        result = stores_collection.find_by_name('Durango')

        assert len(result) == 1
        assert result[0].name == 'Durango'

    def test_it_finds_stores_by_part_of_the_name(self):
        stores_collection = decathlon_stores.DecathlonStores()

        result = stores_collection.find_by_name('Duran')

        assert any(store.name == 'Durango' for store in result)

    def test_it_finds_stores_by_city(self):
        stores_collection = decathlon_stores.DecathlonStores()

        result = stores_collection.find_by_city('Madrid')

        assert all(store.city == 'Madrid' for store in result)

    def test_it_finds_stores_by_part_of_the_city_name(self):
        stores_collection = decathlon_stores.DecathlonStores()

        result = stores_collection.find_by_city('Mad')

        assert any(store.city == 'Madrid' for store in result)

    def test_it_finds_stores_by_zip_code(self):
        stores_collection = decathlon_stores.DecathlonStores()

        result = stores_collection.find_by_zip_code('48200')

        assert all(store.zip_code == '48200' for store in result)

    def test_it_finds_stores_by_part_of_the_zip_code_name(self):
        stores_collection = decathlon_stores.DecathlonStores()

        result = stores_collection.find_by_zip_code('482')

        assert any(store.zip_code == '48200' for store in result)

    def test_it_finds_stores_by_distance_from_a_geo_position(self):
        stores_collection = decathlon_stores.DecathlonStores()

        result = stores_collection.find_by_distance(
            position=GeoPosition(39.5, 2.8),
            radius_in_kilometers=100
        )

        assert all('Mallorca' in store.city for store in result)

    def test_it_returns_store_is_open_or_closed(self):
        self.datetime = patch('decathlon.store.datetime').start()
        store_dict = json.loads(TEST_STORE_JSON)

        store = store_decoder.decode(store_dict)

        self.datetime.now.return_value = datetime(2020, 1, 10, 12, 0)
        assert store.is_open

        self.datetime.now.return_value = datetime(2020, 1, 9, 12, 0)
        assert not store.is_open

        self.datetime.now.return_value = datetime(2020, 1, 10, 5, 0)
        assert not store.is_open


TEST_STORE_JSON = '''
    {
        "store_id": "001", 
        "name": "Test", 
        "contact": {
            "phone": "999 100 100 100", 
            "website": "http://website.com"
        }, 
        "address": {
            "lines": ["Desenganyo 21", null], 
            "country_code": null, 
            "city": "Gotham", 
            "zipcode": "00112"
        },
        "opening_hours": {
            "usual": {
                "1": [{"end": "20:00", "start": "10:00"}], 
                "2": [{"end": "20:00", "start": "10:00"}], 
                "3": [{"end": "20:00", "start": "10:00"}], 
                "5": [{"end": "20:00", "start": "10:00"}], 
                "6": [{"end": "20:00", "start": "10:00"}], 
                "7": [{"end": "19:00", "start": "11:00"}]
            }, 
            "special": {}, 
            "timezone": "Europe/Paris"
        }, 
        "position": [2.642547, 39.572838]
    }
'''
