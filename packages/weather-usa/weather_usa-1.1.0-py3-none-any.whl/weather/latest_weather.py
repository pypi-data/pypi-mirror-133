from __future__ import annotations
import asyncio
import aiohttp
from inflection import underscore
from typing import Union
from datetime import datetime


def latest_surface_observations(latitude: int = 0, longitude: int = 0, station: str = '',
                                imperial: bool = False, start: datetime = '',
                                end: datetime = '', limit: int = None) -> dict:
    """Get the latest surface observations for the closest station."""
    loop = asyncio.get_event_loop()
    if isinstance(start, datetime):
        start = start.isoformat() + '%2B00:00'
    if isinstance (end, datetime):
        end = end.isoformat() + '%2B00:00'

    if isinstance(latitude, tuple) or isinstance(longitude, tuple) or isinstance(station, tuple):
        result = loop.run_until_complete(multiple_surface_obs(latitude, longitude, station,
                                                              imperial, start, end, limit))
    else:
        if not station and not latitude and not longitude:
            raise TypeError("This function expected either a station name, or a latitude and longtitude provided.")
        elif station:
            station = f'https://api.weather.gov/stations/{station}'
        elif not station:
            station = loop.run_until_complete(_get_closest_station(latitude, longitude))

        result = loop.run_until_complete(_calculate_lso(station, imperial, start, end, limit))
    return result


async def multiple_surface_obs(latitude: Union[int, tuple], longitude: Union[int, tuple],
                               station: Union[str, tuple], imperial: bool, start: str, end: str, limit: int):
    if isinstance(station, tuple):
        station = [f'https://api.weather.gov/stations/{station_name}' for station_name in station]
    if isinstance(latitude, tuple) and isinstance(longitude, tuple):
        if len(latitude) != len(longitude):
            raise ValueError("The latitude and longitude tuples need to be of the same length.")

        lat_long = zip(latitude, longitude)
        station_funcs = [_get_closest_station(lat, long) for lat, long in lat_long]
        station = await asyncio.gather(
            *station_funcs
        )

    result_funcs = [_calculate_lso(stat, imperial, start, end, limit) for stat in station]
    results = await asyncio.gather(
        *result_funcs
    )

    result = results[0]
    [result.update(other_result) for other_result in results[1:]]
    return result

async def _get_closest_station(latitude: int, longitude: int) -> str:
    """Gets the closest weather station"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.weather.gov/points/{latitude},{longitude}/stations') as response:
            closest_station = await response.json()
            return closest_station['features'][0]['id']


async def _calculate_lso(station: str, imperial: bool, start: str, end: str, limit: int) -> dict:
    """Finds latest observations"""
    fahrenheit = lambda x: round(x * 1.8 + 32, 5)
    miles = lambda x: round(0.00062137 * x, 5)
    miles_per_hour = lambda x: round(0.621371 * x, 5)
    inches = lambda x: round(39.3701 * x, 5)
    millibars = lambda x: round(x / 100, 5)
    station_name = station.split('/')[-1]
    obs_dct = {station_name: [] if start and end else {}}
    url = station + (f'/observations?start={start}&end={end}' if start and end else '/observations/latest')
    if '?start' in url and '&end' in url and limit:
        url += f'&limit={limit}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response = await response.json(content_type=None)
            if 'status' in response.keys() and response['status'] == 404 and (start and end):
                raise ValueError(f"{station} did not have any "
                                 f"observations from {start} to {end}.")

            if not start and not end:
                for key, val in response['properties'].items():
                    if key in {'temperature', 'dewpoint', 'windDirection', 'windSpeed',
                               'windGust', 'barometricPressure', 'seaLevelPressure',
                               'visibility', 'precipitationLastHour', 'precipitationLast3Hours',
                               'precipitationLast6Hours', 'relativeHumidity', 'windChill',
                               'heatIndex'}:
                        if imperial and 'degC' in val['unitCode'] and val['value']:
                            obs_dct[station_name][underscore(key)] = fahrenheit(val['value'])
                        elif imperial and 'unit:m' in val['unitCode'] and val['value']:
                            if key == 'visibility':
                                obs_dct[station_name][underscore(key)] = miles(val['value'])
                            else:
                                obs_dct[station_name][underscore(key)] = inches(val['value'])
                        elif imperial and 'unit:km_h-1' in val['unitCode'] and val['value']:
                            obs_dct[station_name][underscore(key)] = miles_per_hour(val['value'])
                        elif imperial and 'unit:Pa' in val['unitCode'] and val['value']:
                            obs_dct[station_name][underscore(key)] = millibars(val['value'])
                        else:
                            obs_dct[station_name][underscore(key)] = val['value']
            else:
                for obs in response['features']:
                    obs_dct[station_name].append({})
                    cur_dct = obs_dct[station_name][-1]
                    cur_dct['time'] = datetime.fromisoformat(obs['properties']['timestamp'])
                    for key, val in obs['properties'].items():
                        if key in {'temperature', 'dewpoint', 'windDirection', 'windSpeed',
                                   'windGust', 'barometricPressure', 'seaLevelPressure',
                                   'visibility', 'precipitationLastHour', 'precipitationLast3Hours',
                                   'precipitationLast6Hours', 'relativeHumidity', 'windChill',
                                   'heatIndex'}:
                            if imperial and 'degC' in val['unitCode'] and val['value']:
                                cur_dct[underscore(key)] = fahrenheit(val['value'])
                            elif imperial and 'unit:m' in val['unitCode'] and val['value']:
                                if key == 'visibility':
                                    cur_dct[underscore(key)] = miles(val['value'])
                                else:
                                    cur_dct[underscore(key)] = inches(val['value'])
                            elif imperial and 'unit:km_h-1' in val['unitCode'] and val['value']:
                                cur_dct[underscore(key)] = miles_per_hour(val['value'])
                            elif imperial and 'unit:Pa' in val['unitCode'] and val['value']:
                                cur_dct[underscore(key)] = millibars(val['value'])
                            else:
                                cur_dct[underscore(key)] = val['value']

    return obs_dct


def compare(dct_to_compare: dict) -> dict:
    """Compares dictionary of existing surface observations, as intended to."""
    return {key: sorted([(dct_to_compare[station][key], station) for station in dct_to_compare.keys()],
                        key=lambda x: x[0] if x[0] else 0)
            for key in list(dct_to_compare.values())[0].keys()}