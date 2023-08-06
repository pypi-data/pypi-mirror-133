from enum import Enum


class Weather(Enum):
    snow = 1
    max_temp = 2
    min_temp = 3
    precip = 4
    max_gust = 5
    snow_depth = 6
    min_rh = 7
    max_rh = 8
    max_dewpoint = 9
    min_dewpoint = 10
    min_heat_index = 11
    max_heat_index = 12
    avg_heat_index = 13
