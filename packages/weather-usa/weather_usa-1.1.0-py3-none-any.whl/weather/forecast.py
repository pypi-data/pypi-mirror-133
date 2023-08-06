from __future__ import annotations
import asyncio
import aiohttp
from datetime import datetime

class Forecast:
    def __init__(self, totals: dict, grid_x: int, grid_y: int, cwa: str, city: str, state: str):
        self.totals = totals
        self.simplified_dict = {key: '...' for key in totals.keys()}
        self.grid_x, self.grid_y = grid_x, grid_y
        self.city, self.state = city, state
        self.cwa = cwa

    def __repr__(self):
        return f"Forecast(totals={self.simplified_dict}, grid_x={self.grid_x}, grid_y={self.grid_y}," \
               f" cwa={self.cwa}, city={self.city}, state={self.state})"


def forecast(latitude: float, longitude: float) -> list[Forecast]:
    """Main function for retrieving forecast for a longitude and latitude"""
    loop = asyncio.get_event_loop()
    *information, request = loop.run_until_complete(_get_gridpoint(latitude, longitude))
    res = loop.run_until_complete(_get_forecast(request))
    return Forecast(totals=res, grid_x=information[0], grid_y=information[1],
                    cwa=information[2], city=information[3], state=information[4])


async def _get_gridpoint(latitude: float, longitude: float) -> tuple[int, int, str, str, str, str]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.weather.gov/points/{latitude},{longitude}") as response:
            response = await response.json()
            response = response['properties']
            return response['gridX'], response['gridY'], response['gridId'], \
                   response['relativeLocation']['properties']['city'], \
                   response['relativeLocation']['properties']['state'], \
                   response['forecastGridData']


async def _get_forecast(url: str) -> Forecast:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response = await response.json()
            response = response['properties']
            totals = {}
            for key, val in zip(list(response.keys())[8:], list(response.values())[8:]):
                if isinstance(val, dict):
                    totals[key] = {}
                    for time_dct in val['values']:
                        time = time_dct['validTime'].split('/')[0]
                        totals[key][datetime.fromisoformat(time)] = time_dct['value']

            return totals