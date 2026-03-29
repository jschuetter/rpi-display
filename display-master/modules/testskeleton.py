#!/bin/python
'''
TestModule
Version 1.0

Module History: 
v1.0: 22 May 2025
- Exists solely for testing new features
'''

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from config import FONTS_PATH
# import Components
from src.Components import *
from modules.Module import Module

# Logging
import logging
log = logging.getLogger(__name__)

class TestModule(Module): 

    def __init__(self, matrix, canvas):
        super().__init__(matrix, canvas, doLoop=True, delay=1/30)
        self.components = [
            # Add components here!
        ]