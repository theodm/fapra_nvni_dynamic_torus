from src.plot.draw_torus import ColorModeInformation, draw_torus_2d
from src.torus_creation.random_grid_shared import (
    sh_create_random_normal_2d_grid_network,
)


g = sh_create_random_normal_2d_grid_network(
    width=10,
    height=10,
    num_distinct_information=10,
    mean=5,
    std_dev=2,
    small_world=True,
)

draw_torus_2d(g, width=50, height=50, color_mode=ColorModeInformation(10))
