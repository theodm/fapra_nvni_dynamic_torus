from src.plot.draw_torus import ColorModeNumberOfTimesVisited, SizeModeNone, draw_torus_2d
from src.search.simulation import PredefinedNodesStartPointStrategy, RandomNodeStartPointStrategy, \
    SingleRandomNodeStartPointStrategy, simulate
from src.search.strategy.only_random_walker import OnlyRandomWalkerStrategyParams
from src.torus_creation.random_grid import RandomStrategyParams

res = simulate(
    graph_strategy="random",
    graph_stratey_params=RandomStrategyParams(),
    grid_width=200,
    grid_height=300,
    num_distinct_information=100,
    random_walker_strategy="only_random_walker",
    random_walker_strategy_params=OnlyRandomWalkerStrategyParams(21),
    num_random_walker=5,
    searched_information=50,
    max_steps=1000000,
    random_walker_start_point_strategy=PredefinedNodesStartPointStrategy(
        [(100, 150), (100, 150), (100, 150), (100, 150), (100, 150)]),
)

steps = res["num_steps"]

res2 = simulate(
    graph_strategy="random",
    graph_stratey_params=RandomStrategyParams(),
    grid_width=200,
    grid_height=300,
    num_distinct_information=100,
    random_walker_strategy="only_random_walker",
    random_walker_strategy_params=OnlyRandomWalkerStrategyParams(1),
    num_random_walker=5,
    searched_information=50,
    max_steps=steps,
    random_walker_start_point_strategy=PredefinedNodesStartPointStrategy(
        [(100, 150), (100, 150), (100, 150), (100, 150), (100, 150)]),
)

max_number_of_times_visited = max(
    [res2["graph"].nodes[node]["visited"] for node in res2["graph"].nodes()]
)

print(steps)

draw_torus_2d(
    res["graph"],
    200,
    300,
    ColorModeNumberOfTimesVisited(res["graph"], max_number_of_times_visited),
    SizeModeNone()
)

draw_torus_2d(
    res2["graph"],
    200,
    300,
    ColorModeNumberOfTimesVisited(res["graph"], max_number_of_times_visited),
    SizeModeNone()
)
