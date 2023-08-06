from __future__ import annotations
import asyncio
import aiohttp
from itertools import chain, zip_longest
import inspect
from datetime import datetime


class Alert:
    """Class to show a type of alert."""
    __slots__ = ('coordinates', 'areas_affected', 'affected_zones', 'start_time', 'end_time', 'cwa_issued',
                 'status', 'message_type', 'category', 'severity', 'certainty', 'urgency', 'event',
                 'description', 'instructions')

    def __init__(self, coordinates: list, area_desc: str, zones: list, starts: str, ends: str,
                 cwa: str, status: str, message_type: str, category: str, severity: str, certainty: str,
                 urgency: str, event: str, description: str, instructions: str):
        self.coordinates = list(chain.from_iterable(coordinates)) if coordinates else None
        self.areas_affected = area_desc
        self.affected_zones = zones
        self.start_time = datetime.fromisoformat(starts) if starts else None
        self.end_time = datetime.fromisoformat(ends) if ends else None
        self.cwa_issued = cwa
        self.status = status
        self.message_type = message_type
        self.category = category
        self.severity = severity
        self.certainty = certainty
        self.urgency = urgency
        self.event = event
        self.description = description
        self.instructions = instructions


def alerts(active: bool = True, point: tuple = None, events: tuple = None, start: str = None, end: str = None,
           status: str = None, codes: tuple = None, message_type: str = None, region_type: str = None,
           region: str = None, area: str = None, zone: str = None, urgency: str = None, severity: str = None,
           certainty: str = None, limit: int = None) -> None:
    """Retrieve alerts from the api.weather.gov API with numerous parameters to filter through current alerts."""
    if any((True for param, val in locals().items() if (isinstance(val, tuple) if
    param not in ('point', 'events', 'codes') else (isinstance(val[0], tuple) if val else None)))):
        loop = asyncio.get_event_loop()
        res = loop.run_until_complete(_multiple_alerts(active, point, events, start, end, status, codes, message_type,
                                                       region_type, region, area, zone, urgency, severity,
                                                       certainty, limit))
        return res
    else:
        loop = asyncio.get_event_loop()
        res = loop.run_until_complete(_get_alert(active, point, events, start, end, status, codes, message_type,
                                                 region_type, region, area, zone, urgency, severity, certainty, limit))
        return res


async def _multiple_alerts(active: bool, point: tuple, events: tuple, start: str, end: str,
                           status: str, codes: tuple, message_type: str, region_type: str,
                           region: str, area: str, zone: str, urgency: str, severity: str,
                           certainty: str, limit: int):
    """Recieves multiple alerts"""

    to_list = dict(locals())
    for var, value in to_list.items():
        if not isinstance(value, list) and not isinstance(value, tuple):
            to_list[var] = [value]

    funcs_to_run = [_get_alert(act, poi, even, st, en, stat, code, msg_type,
                               reg_type, reg, ar, zon, urgen, sever, certain, lim) for act, poi, even, st, en,
                                                                                       stat, code, msg_type, reg_type, reg, ar, zon, urgen, sever, certain, lim
                    in zip_longest(
            to_list['active'], to_list['point'], to_list['events'], to_list['start'], to_list['end'],
            to_list['status'], to_list['codes'], to_list['message_type'], to_list['region_type'],
            to_list['region'], to_list['area'], to_list['zone'], to_list['urgency'],
            to_list['severity'], to_list['certainty'], to_list['limit']
        )]
    results = await asyncio.gather(
        *funcs_to_run
    )
    return results


async def _get_alert(active: bool, point: tuple, event: tuple, start: str, end: str,
                     status: str, code: tuple, message_type: str, region_type: str,
                     region: str, area: str, zone: str, urgency: str, severity: str,
                     certainty: str, limit: int):
    """Retrieves the actual alert from the API itself as a helper function that is aysnchronous for speed-ups."""
    return_result = []
    pars = locals()
    url = "https://api.weather.gov/alerts"
    for idx, arg in enumerate(inspect.getargs(_get_alert.__code__).args):
        if str(pars.get(arg)) not in ('None', '0'):
            url += (f'?{arg}=' if not idx else f'&{arg}=')
        results = {True: 'true', False: 'false', None: 'null'}
        if str((res := pars.get(arg))) not in ('None', '0'):
            if isinstance(res, tuple):
                url += r'%2C'.join(tuple(map(str, pars.get(arg))))
            elif res in results.keys():
                url += results[pars.get(arg)]
            else:
                url += pars.get(arg)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response = await response.json()
            if 'detail' in response.keys():
                raise TypeError(response['detail'])
            for alert in response['features']:
                if alert['geometry']:
                    geom = alert['geometry']['coordinates']
                else:
                    geom = None
                temp_resp = alert['properties']
                return_result.append(Alert(area_desc=temp_resp['areaDesc'], zones=temp_resp['affectedZones'],
                                           starts=temp_resp['onset'], ends=temp_resp['expires'],
                                           status=temp_resp['status'], message_type=temp_resp['messageType'],
                                           category=temp_resp['category'], severity=temp_resp['severity'],
                                           certainty=temp_resp['certainty'], description=temp_resp['description'],
                                           urgency=temp_resp['urgency'], event=temp_resp['event'],
                                           cwa=temp_resp['senderName'], instructions=temp_resp['instruction'],
                                           coordinates=geom))

    return return_result