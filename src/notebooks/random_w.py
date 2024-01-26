from src.plot.draw_torus import ColorModeNumberOfTimesVisited, SizeModeNone, draw_torus_2d
from src.search.simulation import PredefinedNodesStartPointStrategy, RandomNodeStartPointStrategy, \
    SingleRandomNodeStartPointStrategy, simulate
from src.search.strategy.only_random_walker import OnlyRandomWalkerStrategyParams
from src.search.strategy.random_walker_3 import RandomWalker3StrategyParams
from src.torus_creation.random_grid import RandomStrategyParams

seed = 73454

res = simulate(
    graph_strategy="random",
    graph_stratey_params=RandomStrategyParams(),
    grid_width=200,
    grid_height=300,
    num_distinct_information=100,
    random_walker_strategy="random_walker_3",
    random_walker_strategy_params=RandomWalker3StrategyParams(
        random_probability=0.5,
        create_edge_strategy="dynamic_similar",
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

res3 = simulate(
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
    max_steps=200 * 300 * 20,
    random_walker_start_point_strategy=RandomNodeStartPointStrategy(),
    graph_seed=seed
)


res4 = simulate(
    graph_strategy="random",
    graph_stratey_params=RandomStrategyParams(),
    grid_width=200,
    grid_height=300,
    num_distinct_information=100,
    random_walker_strategy="random_walker_3",
    random_walker_strategy_params=RandomWalker3StrategyParams(
        random_probability=0.5,
        create_edge_strategy="dynamic_random",
        random_probability_to_create_edge=0,
        length_of_memory=200,
    ),
    num_random_walker=10,
    searched_information=50,
    max_steps=200 * 300 * 20,
    random_walker_start_point_strategy=RandomNodeStartPointStrategy(),
    graph_seed=seed
)


res5 = simulate(
    graph_strategy="random",
    graph_stratey_params=RandomStrategyParams(),
    grid_width=200,
    grid_height=300,
    num_distinct_information=100,
    random_walker_strategy="random_walker_3",
    random_walker_strategy_params=RandomWalker3StrategyParams(
        random_probability=0.5,
        create_edge_strategy="dynamic_similar",
        random_probability_to_create_edge=0,
        length_of_memory=200,
    ),
    num_random_walker=10,
    searched_information=50,
    max_steps=200 * 300 * 20,
    random_walker_start_point_strategy=RandomNodeStartPointStrategy(),
    graph_seed=seed
)

# res contains step_to_number_of_found_nodes, plot all three res as line chart with plotly
# is an dict of a number (on x-axis) to a number (on y-axis)
# x-axis: number of steps
# y-axis: number of found nodes

import plotly.graph_objects as go

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=list(res["step_to_number_of_found_nodes"].keys()),
        y=list(res["step_to_number_of_found_nodes"].values()),
        name="dynamic_similar_0.05"
    )
)

fig.add_trace(
    go.Scatter(
        x=list(res2["step_to_number_of_found_nodes"].keys()),
        y=list(res2["step_to_number_of_found_nodes"].values()),
        name="dynamic_random_0.05"
    )
)

fig.add_trace(
    go.Scatter(
        x=list(res3["step_to_number_of_found_nodes"].keys()),
        y=list(res3["step_to_number_of_found_nodes"].values()),
        name="only_random_walker"
    )
)

fig.add_trace(
    go.Scatter(
        x=list(res4["step_to_number_of_found_nodes"].keys()),
        y=list(res4["step_to_number_of_found_nodes"].values()),
        name="dynamic_random_0"
    )
)

fig.add_trace(
    go.Scatter(
        x=list(res5["step_to_number_of_found_nodes"].keys()),
        y=list(res5["step_to_number_of_found_nodes"].values()),
        name="dynamic_similar_0"
    )
)

fig.update_layout(
    xaxis_title_text='Anzahl der Schritte',
    yaxis_title_text='Anzahl der gefundenen Knoten'
)

fig.show()

#
# max_number_of_times_visited = max(
#     [res2["graph"].nodes[node]["visited"] for node in res2["graph"].nodes()]
# )
#
# print(steps)
#
# draw_torus_2d(
#     res["graph"],
#     200,
#     300,
#     ColorModeNumberOfTimesVisited(res["graph"], max_number_of_times_visited),
#     SizeModeNone()
# )
#
# draw_torus_2d(
#     res2["graph"],
#     200,
#     300,
#     ColorModeNumberOfTimesVisited(res["graph"], max_number_of_times_visited),
#     SizeModeNone()
# )
