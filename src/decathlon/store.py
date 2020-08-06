from dataclasses import dataclass
from datetime import datetime, time
from typing import List


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
