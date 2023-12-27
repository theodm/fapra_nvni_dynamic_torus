
from src.plot.draw_torus import draw_torus_2d
from src.plot.plot_information_distribution import plot_information_distribution
from src.torus_creation.random_grid import create_random_2d_grid_network

num_distinct_information = 50
width = 30
height = 30

g = create_random_2d_grid_network(
    width, height, num_distinct_information=num_distinct_information
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


draw_torus_2d(
    g,
    num_distinct_information=num_distinct_information,
    width=width,
    height=height,
    color_mode="normal",
    target_information=15,
    colormap="inferno",
)

plot_information_distribution(g, num_distinct_information)
