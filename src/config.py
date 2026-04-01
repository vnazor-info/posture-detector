MARGIN = 10  # pixels
ROW_SIZE = 1  # pixels
FONT_SIZE = 0
FONT_THICKNESS = 5
TEXT_COLOR = (255, 0, 0)  # red

import os, sys

def get_resource_path(relative_path):
    # __file__ is inside src/, so .. goes to project root
    return os.path.join(os.path.dirname(__file__), "..", relative_path)