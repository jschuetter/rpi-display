#!/bin/python
'''
weather module
'''

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from matrix_display.modules.Module import Module
from matrix_display.Components import *
from matrix_display.config import FONTS_PATH

import os
from pathlib import Path



# Logging
import logging
log = logging.getLogger(__name__)

# Define class
class Weather(Module): 
    ASSETS_PATH = os.path.join(
        Path(__file__).resolve().parents[0], # Get path to module directory
        'assets'
        )

    def __init__(self, matrix, canvas):
        super().__init__(matrix, canvas, doloop=True, delay=1/16)
        iconPath = os.path.join(self.ASSETS_PATH, 'sunny.bmp'),
        print(iconPath)
        self.icon = Icon( # Conditions icon
            x_=2,
            y_=1,
            path=os.path.join(self.ASSETS_PATH, 'sunny.bmp'),
        )
        self.temp = Text( # Current temp text
            x_=19,
            y_=14,
            text_="72°",
            font="gohufont/gohufont-14.bdf",
            color=(255, 255, 255)
        )
        self.hilo = Text( # Temp hi/lo text
            x_=38,
            y_=15,
            text_="63/32",
            font="basic/5x7.bdf",
            color=(255, 255, 255)
        )
        self.conditions = ScrollingText( # Conditions, precipitation text
            x_=2,
            y_=28,
            text_="Clear, 100% in 23h",
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