from src.plot.draw_torus import ColorModeNumberOfTimesVisited, SizeModeNone, draw_torus_2d, \
    SizeModeHighlightSearchedInformation
from src.search.simulation import PredefinedNodesStartPointStrategy, RandomNodeStartPointStrategy, \
    SingleRandomNodeStartPointStrategy, simulate
from src.search.strategy.only_random_walker import OnlyRandomWalkerStrategyParams
from src.search.strategy.random_walker_3 import RandomWalker3StrategyParams
from src.torus_creation.random_grid import RandomStrategyParams

seed = 1

res = simulate(
    graph_strategy="random",
    graph_stratey_params=RandomStrategyParams(),
    grid_width=200,
    grid_height=300,
    num_distinct_information=100,
    random_walker_strategy="random_walker_3",
    random_walker_strategy_params=RandomWalker3StrategyParams(
        random_probability=0.5,
        create_edge_strategy="dynamic_random",
        random_probability_to_create_edge=0.05,
        length_of_memory=200,
    ),
    num_random_walker=10,
    searched_information=50,
    max_steps=200 * 300 * 20,
    random_walker_start_point_strategy=RandomNodeStartPointStrategy(),
    graph_seed=seed
)

steps = res["num_steps"]

res2 = simulate(
    graph_strategy="random",
    graph_stratey_params=RandomStrategyParams(),
    grid_width=200,
    grid_height=300,
    num_distinct_information=100,
    random_walker_strategy="only_random_walker",
    random_walker_strategy_params=OnlyRandomWalkerStrategyParams(
        length_of_memory=200,
    ),
    num_random_walker=10,
    searched_information=50,
    max_steps=steps,
    random_walker_start_point_strategy=RandomNodeStartPointStrategy(),
    graph_seed=seed
)

max_number_of_times_visited = max(
    max(
        [res2["graph"].nodes[node]["visited"] for node in res2["graph"].nodes()]
    ),
    max(
        [res["graph"].nodes[node]["visited"] for node in res["graph"].nodes()]
    )
)

print(f"dyn {steps}")
print(f"ran {res2['num_steps']}")

draw_torus_2d(
    res["graph"],
    200,
    300,
    ColorModeNumberOfTimesVisited(res["graph"], max_number_of_times_visited),
    SizeModeHighlightSearchedInformation(searched_information=50),
    False
)

draw_torus_2d(
    res2["graph"],
    200,
    300,
    ColorModeNumberOfTimesVisited(res2["graph"], max_number_of_times_visited),
    SizeModeHighlightSearchedInformation(searched_information=50),
    False
)
