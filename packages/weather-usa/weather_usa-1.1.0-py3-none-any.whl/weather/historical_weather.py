import asyncio
import aiohttp
from datetime import datetime
from weather_types import Weather
from typing import Union


states = """
Alabama	AL
Alaska	AK
Arizona	AZ
Arkansas	AR
California	CA
Colorado	CO
Connecticut	CT
Delaware	DE
Florida	FL
Georgia	GA
Hawaii	HI
Idaho	ID
Illinois	IL
Indiana	IN
Iowa	IA
Kansas	KS
Kentucky	KY
Louisiana	LA
Maine	ME
Maryland	MD
Massachusetts	MA
Michigan	MI
Minnesota	MN
Mississippi	MS
Missouri	MO
Montana	MT
Nebraska	NE
Nevada	NV
New Hampshire	NH
New Jersey	NJ
New Mexico	NM
New York	NY
North Carolina	NC
North Dakota	ND
Ohio	OH
Oklahoma	OK
Oregon	OR
Pennsylvania	PA
Rhode Island	RI
South Carolina	SC
South Dakota	SD
Tennessee	TN
Texas	TX
Utah	UT
Vermont	VT
Virginia	VA
Washington	WA
West Virginia	WV
Wisconsin	WI
Wyoming	WY
"""
abbreviations = {l.strip('\n').lower(): k.strip('\n') for l, k in
                     [(line.split('\t')[0],line.split('\t')[-1].strip('\n')) for line in states]}
abbreviations.update({'district of columbia': 'DC'})

abbreviations_change = {state: abbr for state, abbr in zip(abbreviations.values(), abbreviations.keys())}


class HistoricalWeatherData:
    def __init__(self, airport, state):
        self.airport = airport.lstrip('K')
        self.state = state if len(state) == 2 else abbreviations[state.lower()]

    async def _calculate(self, date: tuple, enum_type: Weather) -> dict:
        """Calculate the requested historical data"""
        if isinstance(date, int) or isinstance(date, str):
            raise ValueError("Tuple expected for date parameter.\n\n"
                             f"Did you mean: ...generate(({date},), {enum_type})")
        mapping_key = {Weather.max_temp: 'max_tmpf', Weather.min_temp: 'min_tempf',
                       Weather.precip: 'precip', Weather.max_gust: 'max_gust', Weather.snow: 'snow',
                       Weather.snow_depth: 'snowd', Weather.min_rh: 'min_rh', Weather.max_rh: 'max_rh',
                       Weather.max_dewpoint: 'max_dwpf', Weather.min_dewpoint: 'min_dwpf',
                       Weather.max_heat_index: 'max_feel', Weather.min_heat_index: 'min_feel',
                       Weather.avg_heat_index: 'avg_feel'}
        enum_type = mapping_key[enum_type]
        async with aiohttp.ClientSession() as session:
            url = self.generate_url(date)
            async with session.get(url) as response:
                iem_request = await response.json()
                iem_request = iem_request['data']
                expr = {datetime.strptime(data['date'], '%Y-%m-%d'): data[enum_type]
                        for data in iem_request if data[enum_type]}
                return expr

    async def _get_total_snow(self, date: tuple, type: Union[tuple[Weather], Weather]):
        if isinstance(type, tuple):
            all_res = [self._calculate(date, enum_type) for enum_type in type]
        else:
            all_res = [self._calculate(date, type)]
            type = [type]

        total = await asyncio.gather(*all_res)
        total_dct = {}
        for result, type_wanted in zip(total, type):
            total_dct[type_wanted.name] = result

        return total_dct

    def generate(self, date: tuple, type: Union[tuple[Weather], Weather]):
        loop = asyncio.get_event_loop()
        data = loop.run_until_complete(self._get_total_snow(date, type))
        return data

    def generate_url(self, date: tuple) -> str:
        """Generates url for self._calculate"""
        if len(date) == 3:
            if len(str(date[1])) == 1:
                date = list(date)
                date[1] = '0' + str(date[1])
            url = f"https://mesonet.agron.iastate.edu/api/1/" \
                  f"daily.json?date={date[0]}-{date[1]}-{date[2]}&" \
                  f"station={self.airport}&network={self.state}_ASOS"
        elif len(date) == 2:
            if len(str(date[1])) == 1:
                date = list(date)
                date[1] = '0' + str(date[1])
            url = f"https://mesonet.agron.iastate.edu/api/1/daily.json?" \
                  f"station={self.airport}&network={self.state}_ASOS&year={date[0]}&month={date[1]}"
        else:
            url = f'https://mesonet.agron.iastate.edu/api/1/daily.json?' \
                  f'station={self.airport}&network={self.state}_ASOS&year={date[0]}'

        return url
