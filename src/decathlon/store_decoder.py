from datetime import time

from decathlon.store import Store, GeoPosition, OpeningHour


STORES_JSON_WEEK_DAY_OFFSET = 1


def decode(store_dict):
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
