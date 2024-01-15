
from src.plot.draw_torus import ColorModeNumberOfTimesVisited, SizeModeNone, draw_torus_2d
from src.search.simulation import PredefinedNodesStartPointStrategy, RandomNodeStartPointStrategy, SingleRandomNodeStartPointStrategy, simulate
from src.search.strategy.only_random_walker import OnlyRandomWalkerStrategyParams
from src.torus_creation.random_grid import RandomStrategyParams


res = simulate(
    graph_strategy="random",
    graph_stratey_params=RandomStrategyParams(),
    grid_width=200,
    grid_height=300,
    num_distinct_information=100,
    random_walker_strategy="only_random_walker",
    random_walker_strategy_params=OnlyRandomWalkerStrategyParams(100),
    num_random_walker=1,
    searched_information=50,
    max_steps=10000,
    random_walker_start_point_strategy=PredefinedNodesStartPointStrategy([(100, 150)]),
)

draw_torus_2d(
    res["graph"],
    200,
    300,
    ColorModeNumberOfTimesVisited(res["graph"]),
    SizeModeNone()
)