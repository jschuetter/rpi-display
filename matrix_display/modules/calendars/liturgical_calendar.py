#!/bin/python
'''
liturgical calendar module
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
from datetime import date, timedelta
from pypdf import PdfReader

# Logging
import logging
log = logging.getLogger(__name__)

# Define class
class LiturgicalCalendar(Module): 
    RESOURCES_PATH = os.path.join(
        Path(__file__).resolve().parents[0], # Get path to module directory
        'resources'
        )

    def __init__(self, matrix, canvas):
        super().__init__(matrix, canvas, doloop=True, delay=1/16)

        # Load current calendar