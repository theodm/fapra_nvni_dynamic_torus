from src.search.simulation import RandomNodeStartPointStrategy, simulate
from src.search.strategy.only_random_walker import OnlyRandomWalkerStrategyParams
from src.search.strategy.random_walker_3 import RandomWalker3StrategyParams
from src.torus_creation.random_grid import RandomStrategyParams

def dynamic_random_creator(create_edge_strategy, random_probability):
    def stragey_fn(edge_prob):
        random_walker_strategy_params = RandomWalker3StrategyParams(
            random_probability=random_probability,
            create_edge_strategy=create_edge_strategy,
            random_probability_to_create_edge=edge_prob,
            length_of_memory=200,
        )

        return "random_walker_3", random_walker_strategy_params

    return stragey_fn

straegy_to_fn = {
    "dynamic_random_0.5": dynamic_random_creator("dynamic_random", 0.5),
    "dynamic_similar_0.5": dynamic_random_creator("dynamic_similar", 0.5),
}



from joblib import Memory, Parallel, delayed

memory = Memory("cachedir", verbose=0)

@memory.cache
def execute_sim(strategy, edge_prob):
    # disable loguru logging
    import loguru
    loguru.logger.remove()

    results = []

    strategy_name, strategy_params = straegy_to_fn[strategy](edge_prob)

    for i in range(1000):
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

        results.append(
            {
                "num_steps": res["num_steps"],
                "edges_added": res["edges_added"]
            }
        )

    av = sum([r["num_steps"] for r in results]) / len(results)
    # return std_dev
    stddev = (sum([(r["num_steps"] - av)**2 for r in results]) / len(results))**0.5
    # return min, max
    _min = min([r["num_steps"] for r in results])
    _max = max([r["num_steps"] for r in results])

    edges_added_av = sum([r["edges_added"] for r in results]) / len(results)

    return av, stddev, _min, _max, edges_added_av



def compute_result2(strategy, edge_prob):
    print(f"Computing {strategy} {edge_prob}")
    av, stddev, _min, _max, edges_added_av = execute_sim(strategy, edge_prob)

    print(f"{strategy} {edge_prob} av: {av} stddev: {stddev} min: {_min} max: {_max} edges_added_av: {edges_added_av}")

    return {
        "edge_prob": str(edge_prob),
        "strategy": strategy,
        "av": av,
        "stddev": stddev,
        "min": _min,
        "max": _max,
        "edges_added_av": edges_added_av,
    }

# Create a list of all combinations of strategies and lengths of memory
inputs = [(strategy, edge_prob * 0.005) for strategy in straegy_to_fn for edge_prob in range(0, 30)]

# Use joblib to parallelize the computation
results = Parallel(n_jobs=-1)(delayed(compute_result2)(strategy, edge_prob) for strategy, edge_prob in inputs)

res = {}

for result in results:
    if result["edge_prob"] not in res:
        res[result["edge_prob"]] = {}

    res[result["edge_prob"]][result["strategy"]] = result


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
    x = sorted([float(edge_prob) for edge_prob in res])

    y = []
    for l in x:
        y.append(res[str(l)][strategy]["av"])

    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=strategy))

fig.show()