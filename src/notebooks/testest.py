from src.search.simulation import plot_single_result, simulate
from src.search.strategy.random_walker_1 import RandomWalker1StrategyParams

res = simulate(
    graph_strategy="random_normal_variate",
    grid_width=40,
    grid_height=40,
    num_distinct_information=100,
    random_walker_strategy="random_walker_1",
    random_walker_strategy_params=RandomWalker1StrategyParams(
        random_probability=0.9,
        random_probability_of_adding_edge=0.005,
        length_of_memory=150,
    ),
    num_random_walker=10,
    searched_information=49,
    max_steps=5000,
)

plot_single_result(res)