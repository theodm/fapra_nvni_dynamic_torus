# %%
from typing import Literal

import plotly.express as px
import plotly.graph_objects as go
import networkx
from math import pi, cos, sin
import random

from src.colormap import colormap_for_information
from src.draw_torus import draw_torus_3d, draw_torus_2d
from src.ranged_int.ranged_int import ClampedInt, OverflowInt
from src.torus_creation.blobs_increase_grid import (
    create_random_2d_grid_network_constant_blob_increase,
)
from src.torus_creation.image_grid import create_2d_grid_from_image
from src.torus_creation.information_blobs_grid import (
    create_random_2d_grid_network_information_blobs,
)
from src.torus_creation.information_lines_grid import (
    create_random_2d_grid_network_information_lines,
)
from src.torus_creation.lines_increase_grid import (
    create_random_2d_grid_network_constant_lines_increase,
)
from src.torus_creation.random_grid import create_random_2d_grid_network
from src.torus_creation.random_walker_grid import create_random_2d_grid_random_walkers

num_distinct_information = 50

g = create_random_2d_grid_network(
    30, 30, num_distinct_information=num_distinct_information
)
# g = create_random_2d_grid_network_constant_blob_increase(
#     100,
#     100,
#     blob_radius=10,
#     num_distinct_information=num_distinct_information,
#     num_blobs=10000,
#     int_mode="overflow",
# )
# g = create_random_2d_grid_network_information_blobs(
#     200,
#     300,
#     blob_radius=10,
#     num_distinct_information=num_distinct_information,
#     num_blobs=250,
#     information_blobs=[3, 6, 9],
#     blob_radius_decrease_factor=1,
#     int_mode="overflow",
# )
# g = create_random_2d_grid_network_constant_lines_increase(
#     200,
#     300,
#     num_distinct_information=num_distinct_information,
#     num_lines=250,
#     line_radius=10,
#     int_mode="overflow",
# )
# g = create_random_2d_grid_network_information_lines(
#     200,
#     300,
#     line_radius=10,
#     num_distinct_information=num_distinct_information,
#     num_lines=250,
#     information_lines=[3, 6, 9],
#     line_radius_decrease_factor=1,
#     int_mode="overflow",
# )
# g = create_random_2d_grid_random_walkers(
#     100,
#     100,
#     num_distinct_information=num_distinct_information,
#     num_random_walkers=70,
#     num_steps=500,
#     radius_min=1,
#     radius_max=4,
#     special_radius_min=5,
#     special_radius_max=20,
#     increase_multiplier=15,
#     int_mode="overflow",
# )

# Zufällige Kanten im Graphen hinzufügen
for i in range(10):
    g.add_edge(
        random.choice(list(g.nodes())),
        random.choice(list(g.nodes())),
    )

draw_torus_2d(
    g,
    num_distinct_information=num_distinct_information,
    width=30,
    height=30,
    color_mode="normal",
    target_information=90,
    colormap="inferno",
)
