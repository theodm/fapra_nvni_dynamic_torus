from src.plot.plot_information_distribution import plot_information_distribution
from src.torus_creation.random_grid import create_random_2d_grid_network_normal_with_params, RandomNormalStrategyParams, \
    create_random_2d_grid_network_with_params

# Für die Präsentation

# g = create_random_2d_grid_network_normal_with_params(
#     width=200,
#     height=300,
#     num_distinct_information=100,
#     params=RandomNormalStrategyParams.default(
#         num_distinct_information=100
#     )
# )
#
# plot_information_distribution(g, 100)

g = create_random_2d_grid_network_with_params(
    width=200,
    height=300,
    num_distinct_information=100,
    params=None
)

plot_information_distribution(g, 100)
