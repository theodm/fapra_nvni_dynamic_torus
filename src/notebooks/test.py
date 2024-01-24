#%%
from src.search.simulation import plot_single_result, simulate, RandomNodeStartPointStrategy
from src.search.strategy.random_walker_1 import RandomWalker1StrategyParams
from src.search.strategy.random_walker_3 import RandomWalker3StrategyParams
from src.torus_creation.random_grid import RandomNormalStrategyParams, RandomStrategyParams

grid_width_height = 25

res = simulate(
    graph_strategy="random",
    graph_stratey_params=RandomStrategyParams(),
    grid_width=grid_width_height,
    grid_height=grid_width_height,
    num_distinct_information=100,
    random_walker_strategy="random_walker_3",
    random_walker_strategy_params=RandomWalker3StrategyParams(
        random_probability=0.5,
        create_edge_strategy="dynamic_similar",
        random_probability_to_create_edge=0.1,
        length_of_memory=200,
    ),
    num_random_walker=5,
    searched_information=50,
    max_steps=50000,
    random_walker_start_point_strategy=RandomNodeStartPointStrategy(),
)

plot_single_result(res)
# %%
