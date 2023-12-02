from src.search.simulation import plot_single_result, simulate
from src.search.strategy.only_random_walker import OnlyRandomWalkerStrategyParams
from src.search.strategy.random_walker_1 import RandomWalker1StrategyParams
from src.search.strategy.random_walker_2 import RandomWalker2StrategyParams
from src.torus_creation.random_grid import (
    RandomNormalStrategyParams,
    RandomStrategyParams,
)


res = simulate(
    graph_strategy="random",
    graph_stratey_params=RandomStrategyParams(),
    grid_width=40,
    grid_height=40,
    num_distinct_information=100,
    random_walker_strategy="only_random_walker",
    random_walker_strategy_params=OnlyRandomWalkerStrategyParams(),
    num_random_walker=10,
    searched_information=49,
    max_steps=5000,
)

plot_single_result(res)
