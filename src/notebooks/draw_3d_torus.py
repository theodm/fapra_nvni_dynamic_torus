from src.plot.draw_torus import draw_torus_3d, ColorModeInformation, SizeModeHighlightSearchedInformation
from src.torus_creation.random_grid import create_random_2d_grid_network_with_params

g = create_random_2d_grid_network_with_params(
    width=60,
    height=90,
    num_distinct_information=100,
    params=None
)

draw_torus_3d(
    g,
    ColorModeInformation(100),
    SizeModeHighlightSearchedInformation(50),
)