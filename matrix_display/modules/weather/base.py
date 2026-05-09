#!/bin/python
'''
weather module
'''

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from matrix_display.modules.Module import Module
from matrix_display.Components import *
from matrix_display.config import FONTS_PATH
from . import settings

import os
from pathlib import Path
import requests
from datetime import datetime as dt

# Logging
import logging
log = logging.getLogger(__name__)

# Define class
class Weather(Module): 
    ASSETS_PATH = os.path.join(
        Path(__file__).resolve().parents[0], # Get path to module directory
        'assets'
        )
    ICON_CODE_MAP = {
        113: None, # Clear
        116: None,  # Partly
        119: "cloudy.bmp",
        122: "cloudy.bmp",
        143: "fog.bmp",
        176: None,
        179: None,
        182: None,
        185: None,
        200: None,
        227: "snow.bmp",
        230: "snow.bmp",
        248: "fog.bmp",
        260: "fog.bmp",
        263: "rainmbp",
        266: "rain.bmp",
        281: "rain.bmp",
        284: "rain.bmp",
        293: "rain.bmp",
        296: "rain.bmp",
        299: "rain.bmp",
        302: "rain.bmp",
        305: "rain.bmp",
        308: "rain.bmp",
        311: "rain.bmp",
        314: "rain.bmp",
        317: "rain.bmp",
        320: "rain.bmp",
        323: "snow.bmp",
        326: "snow.bmp",
        329: "snow.bmp",
        332: "snow.bmp",
        335: "snow.bmp",
        338: "snow.bmp",
        350: "snow.bmp",
        353: "rain.bmp",
        356: "rain.bmp",
        359: "rain.bmp",
        362: "rain.bmp",
        365: "rain.bmp",
        368: "rain.bmp",
        371: "snow.bmp",
        374: "snow.bmp",
        377: "snow.bmp",
        386: "thunder.bmp",
        389: "thunder.bmp",
        392: "thunder.bmp",
        395: "thunder.bmp",
    }
    MOON_PHASE_MAP = {
        "New": "new",
        "Waxing Crescent": "crescent-waxing",
        "First Quarter": "q1",
        "Waxing Gibbous": "gib-waxing",
        "Full": "full",
        "Waning Gibbous": "gib-waning",
        "Last Quarter": "q3",
        "Waning Crescent": "crescent-waning",
    }

    def __init__(self, matrix, canvas):
        super().__init__(matrix, canvas, doloop=True, delay=1/16)

        # Fetch data for components
        api_url = 'https://wttr.in/'
        if settings.locale is not None: 
            api_url += settings.locale
        api_url += '?format=j1'

        response = requests.get(api_url)
        data = response.json()

        self.icon = Icon( # Conditions icon
            x_=2,
            y_=1,
            path=os.path.join(self.ASSETS_PATH, self.get_icon_path(data)),
        )
        self.temp = Text( # Current temp text
            x_=19,
            y_=14,
            text_=f"{data['current_condition'][0]['FeelsLikeF']}°",
            font="gohufont/gohufont-14.bdf",
            color=(255, 255, 255)
        )
        self.hilo = Text( # Temp hi/lo text
            x_=38,
            y_=15,
            text_=f"{data['weather'][0]['maxtempF']}/{data['weather'][0]['mintempF']}",
            font="basic/5x7.bdf",
            color=(255, 255, 255)
        )
        self.conditions = ScrollingText( # Conditions, precipitation text
            x_=2,
            y_=28,
            text_=get_conditions_str(data),
            font="basic/5x7.bdf",
            color=(255, 255, 255),
            delay=40
        )
        self.components = [
            self.icon,
            self.temp,
            self.hilo,
            self.conditions
        ]

    @classmethod
    def get_icon_path(cls, data_json):
        '''
        Helper method to get path for icon
        corresponding to current conditions
        '''
        condition_code = int(data_json['current_condition'][0]['weatherCode'])
        path = cls.ICON_CODE_MAP[condition_code]
        if path is not None: 
            return path
        else: 
            now = dt.now()
            sunup = dt.strptime(
                data_json['weather'][0]['astronomy'][0]['sunrise'],
                '%I:%M %p'
            )
            sundown = dt.strptime(
                data_json['weather'][0]['astronomy'][0]['sunset'],
                '%I:%M %p'
            )
            is_day = sunup.time() < now.time() < sundown.time()
            (moon_phase,) = data_json['weather'][0]['astronomy'][0]['moon_phase'],
            if condition_code == 113: # Clear
                # Get time of day or moon phase
                if is_day: 
                    return "sunny.bmp"
                else: 
                    return f"night-{cls.MOON_PHASE_MAP[moon_phase]}.bmp"
            else: # Partly cloudy
                if is_day: 
                    return "ptlyCloudy.bmp"
                else: 
                    return f"night-{cls.MOON_PHASE_MAP[moon_phase]}-cloudy.bmp"

def get_conditions_str(data_json): 
    '''
    Helper method to generate conditions string for bottom
    of display, with current conditions descriptor and 
    next precipitation
    '''
    next_precip = get_next_precip(data_json)
    cond_str = f"{data_json['current_condition'][0]['weatherDesc'][0]['value']}, {next_precip}"
    return cond_str

def get_next_precip(data_json): 
    '''
    Helper method to find next chance of precipitation, 
    given JSON repsonse from wttr.in API

    Returns a string in one of the following formats: 
        "XX% chance of rain/snow"   (if current chance of rain/snow)
        "XX% in 00h (rain/snow)"    (if future chance of rain)
        "dry for 3 days"                (if no chance of rain in forecast)
    '''
    now = dt.now()
    current_time_int = int(now.strftime('%H%M'))

    chance_pct = None
    chance_day = None
    chance_time_int = None
    chance_type = None

    for day_idx in range(3): 
        day = data_json['weather'][day_idx]
        for hour_idx in range(8): 
            hour = day['hourly'][hour_idx]
            time_int = int(hour['time'])

            if day_idx == 0 and time_int < current_time_int: 
                # Skip any hours that have already passed
                continue

            if hour['chanceofrain'] != "0": 
                chance_pct = int(hour['chanceofrain'])
                chance_day = day_idx
                chance_time_int = time_int
                chance_type = 'rain'
            elif hour['chanceofsnow'] != "0":
                chance_pct = int(hour['chanceofsnow'])
                chance_day = day_idx
                chance_time_int = time_int
                chance_type = 'snow'

            if chance_pct is not None:
                # Calculate timediff in next chance (in hours)
                timediff = 0
                if chance_day == 0: 
                    timediff = chance_time_int - current_time_int // 100
                else: 
                    timediff = (
                        (2400 - current_time_int) + # Time remaining in current day
                        chance_time_int +           # Time in day with chance
                        (2400 * (chance_day - 1))   # Additional days between now and chance
                    ) // 100
                
                if timediff < 3: 
                    return f"{chance_pct}% chance of {chance_type}"
                elif timediff < 24: 
                    return f"{chance_pct}% in {timediff}h ({chance_type})"
                else: 
                    return f"{chance_pct}% in {timediff//24}d ({chance_type})"
            else: 
                # No chance of rain found
                return "dry for 3 days"