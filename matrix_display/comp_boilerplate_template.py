#!/bin/python
'''
$compname module
'''

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from matrix_display.modules.Module import Module
from matrix_display.Components import *
from matrix_display.config import FONTS_PATH
$imports

# Logging
import logging
log = logging.getLogger(__name__)

# Define class
class $compname(Module): 

    def __init__(self, matrix, canvas):
        super().__init__(matrix, canvas$kwargs)
        self.components = [