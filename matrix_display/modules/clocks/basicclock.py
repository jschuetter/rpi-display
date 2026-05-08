#!/bin/python
'''
BasicClock module
Version 2.2

Module History: 
v1.0: 19 Jun 2024
- Basic functionality
v2.0: 12 Feb 2025
- Port to "class" model for module handler
- Renamed `loop` to `draw`, referred `loop` to `draw` (15 Feb)
'''

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from matrix_display.modules.Module import Module
from matrix_display.Components import DateTimeDisplay
from datetime import datetime as dt
import time, pytz
from matrix_display.config import FONTS_PATH

# Logging
import logging
log = logging.getLogger(__name__)

# Class constants
DATE_X = 2
DATE_Y = 8
DATE_FORMAT = "%b %d, %Y"

TIME_X = 5
TIME_Y = 25
TIME_FORMAT_24 = "%H:%M:%S"
TIME_FORMAT_12 = "%I:%M %p"

MILITARY_TIME = True 
TZ_EST = pytz.timezone("US/Eastern")

# Fonts
TIME_FONT_PATH = "basic/7x13B.bdf"
DATE_FONT_PATH = "basic/5x7.bdf"
FONT_COLOR = (255,255,255)

# Define BasicClock as class
class BasicClock(Module): 

    def __init__(self, matrix, canvas):
        super().__init__(matrix, canvas, doloop=True, delay=1)
        self.components = [
            # Date display
            DateTimeDisplay(
                DATE_X, DATE_Y,
                font=DATE_FONT_PATH,
                color=FONT_COLOR,
                rightAlign=False,
                dtFormat=DATE_FORMAT 
            ),
            # Time display
            DateTimeDisplay(
                TIME_X, TIME_Y,
                font=TIME_FONT_PATH,
                color=FONT_COLOR,
                rightAlign=False,
                dtFormat=TIME_FORMAT_24 if MILITARY_TIME else TIME_FORMAT_12
            )
        ]