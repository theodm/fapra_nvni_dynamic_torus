from src.search.simulation import RandomNodeStartPointStrategy, simulate
from src.search.strategy.only_random_walker import OnlyRandomWalkerStrategyParams
from src.search.strategy.random_walker_3 import RandomWalker3StrategyParams
from src.torus_creation.random_grid import RandomStrategyParams


def random_memory(length_of_memory):
    return "only_random_walker", OnlyRandomWalkerStrategyParams(
        length_of_memory=length_of_memory,
    )



def dynamic_random_creator(create_edge_strategy, random_probability, random_probabilty_of_adding_edge):
    def stragey_fn(length_of_memory):
        random_walker_strategy_params = RandomWalker3StrategyParams(
            random_probability=random_probability,
            create_edge_strategy=create_edge_strategy,
            random_probability_to_create_edge=random_probabilty_of_adding_edge,
            length_of_memory=length_of_memory,
        )

        return "random_walker_3", random_walker_strategy_params

    return stragey_fn

straegy_to_fn = {
    "random_memory": random_memory,
    "dynamic_random_0.5_0.0": dynamic_random_creator("dynamic_random", 0.5, 0.0),
    "dynamic_random_0.5_0.005": dynamic_random_creator("dynamic_random", 0.5, 0.005),
    "dynamic_random_0.5_0.01": dynamic_random_creator("dynamic_random", 0.5, 0.01),
    "dynamic_random_0.5_0.03": dynamic_random_creator("dynamic_random", 0.5, 0.03),
    "dynamic_random_0.5_0.05": dynamic_random_creator("dynamic_random", 0.5, 0.05),
    "dynamic_random_0.5_0.1": dynamic_random_creator("dynamic_random", 0.5, 0.1),
    "dynamic_similar_0.5_0.0": dynamic_random_creator("dynamic_similar", 0.5, 0.0),
    "dynamic_similar_0.5_0.005": dynamic_random_creator("dynamic_similar", 0.5, 0.005),
    "dynamic_similar_0.5_0.01": dynamic_random_creator("dynamic_similar", 0.5, 0.01),
    "dynamic_similar_0.5_0.03": dynamic_random_creator("dynamic_similar", 0.5, 0.03),
    "dynamic_similar_0.5_0.05": dynamic_random_creator("dynamic_similar", 0.5, 0.05),
    "dynamic_similar_0.5_0.1": dynamic_random_creator("dynamic_similar", 0.5, 0.1),
}



from joblib import Memory, Parallel, delayed

memory = Memory("cachedir", verbose=0)

@memory.cache
def execute_sim(strategy, length_of_memory):
    # disable loguru logging
    import loguru
    loguru.logger.remove()

    results = []

    strategy_name, strategy_params = straegy_to_fn[strategy](length_of_memory)

    for i in range(200):
        # calculate graph_seed from random_probability, random_probability_of_adding_edge, length_of_memory, num_random_walker, i but not create_edge_strategy
        graph_seed = hash(i) % (2 ** 32)

        res = simulate(
            graph_strategy="random",
            graph_stratey_params=RandomStrategyParams(),
            grid_width=100,
            grid_height=100,
            num_distinct_information=100,
            random_walker_strategy=strategy_name,
            random_walker_strategy_params=strategy_params,
            num_random_walker=10,
            searched_information=50,
            max_steps=100*100*10,
            random_walker_start_point_strategy=RandomNodeStartPointStrategy(),
            graph_seed=graph_seed
        )

        results.append(res)

    av = sum([r["num_steps"] for r in results]) / len(results)
    # return std_dev
    stddev = (sum([(r["num_steps"] - av)**2 for r in results]) / len(results))**0.5
    # return min, max
    _min = min([r["num_steps"] for r in results])
    _max = max([r["num_steps"] for r in results])

    return av, stddev, _min, _max



def compute_result(strategy, length_of_memory):
    av, stddev, _min, _max, = execute_sim(strategy, length_of_memory)

    print(f"{strategy} {length_of_memory} av: {av} stddev: {stddev} min: {_min} max: {_max}")

    return {
        "length_of_memory": str(length_of_memory),
        "strategy": strategy,
        "av": av,
        "stddev": stddev,
        "min": _min,
        "max": _max,
    }

# Create a list of all combinations of strategies and lengths of memory
inputs = [(strategy, length_of_memory) for strategy in straegy_to_fn for length_of_memory in range(1, 510, 10)]

# Use joblib to parallelize the computation
results = Parallel(n_jobs=-1)(delayed(compute_result)(strategy, length_of_memory+1) for strategy, length_of_memory in inputs)

res = {}

for result in results:
    if result["length_of_memory"] not in res:
        res[result["length_of_memory"]] = {}

    res[result["length_of_memory"]][result["strategy"]] = result


print(results)

# show diagram with length_of_memory as x-axis and av as y-axis
# each strategy as a line
#
# import matplotlib.pyplot as plt
#
# for strategy in straegy_to_fn:
#     x = sorted([int(length_of_memory) for length_of_memory in res])
#
#     y = []
#     for l in x:
#         y.append(res[str(l)][strategy]["av"])
#
#     plt.plot(x, y, label=strategy)
#
# plt.legend()
# plt.show()

import plotly.graph_objects as go
fig = go.Figure()

for strategy in straegy_to_fn:
    x = sorted([int(length_of_memory) for length_of_memory in res])

    y = []
    for l in x:
        y.append(res[str(l)][strategy]["av"])

    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=strategy))

fig.show()