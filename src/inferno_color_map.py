
from colour import Color
import seaborn as sns
import numpy as np

import matplotlib
import matplotlib.cm as cm

rgba = cm.inferno

def inferno(number_of_distinct_colors):
    colors = []
    for i in range(0, number_of_distinct_colors):
        r = i * 1.0 / number_of_distinct_colors
        
        colors.append(Color(rgb = rgba(r)[:3]).get_hex_l())

    return colors

