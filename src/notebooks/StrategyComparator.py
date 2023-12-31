from statistics import stdev

from src.search.simulation import simulate
from src.search.strategy.only_random_walker import OnlyRandomWalkerStrategyParams
from src.search.strategy.random_walker_1 import RandomWalker1StrategyParams
from src.search.strategy.random_walker_2 import RandomWalker2StrategyParams
from src.torus_creation.random_grid import RandomStrategyParams

import pandas as pd
import time
from joblib import Parallel, delayed

# Logging deaktivieren, denn das macht hier keinen Sinn und bläht die Konsole nur auf
# stattdessen einfach in eine Log-Datei
import loguru

loguru.logger.remove()
loguru.logger.add("strategy_comparator.log", level="ERROR")


def print_info_for_attribute(objs, attribute_name):
    print("attribute_name: ", attribute_name)
    avg = sum([r[attribute_name] for r in objs]) / len(objs)
    _min = min([r[attribute_name] for r in objs])
    _max = max([r[attribute_name] for r in objs])
    std_dev = stdev([r[attribute_name] for r in objs])

    print(f"avg: {avg}")
    print(f"min: {_min}")
    print(f"max: {_max}")
    print(f"std_dev: {std_dev}")
    print(f"")


def print_for_result(name, runs):
    def min_max_avg_std_dev_for_runs(runs, attribute_name):
        avg = sum([r[attribute_name] for r in runs]) / len(runs)
        _min = min([r[attribute_name] for r in runs])
        _max = max([r[attribute_name] for r in runs])
        std_dev = stdev([r[attribute_name] for r in runs])

        return {
            f"{attribute_name}_avg": avg,
            f"{attribute_name}_min": _min,
            f"{attribute_name}_max": _max,
            f"{attribute_name}_std_dev": std_dev,
        }

    return {
        "name": name,
        **min_max_avg_std_dev_for_runs(runs, "num_steps"),
        **min_max_avg_std_dev_for_runs(runs, "num_found_nodes"),
        **min_max_avg_std_dev_for_runs(runs, "num_searched_nodes"),
        "num_times_out_of_steps": sum(
            [(0 if r["break_type"] == "all_found" else 1) for r in runs]
        ),
        "num_times": len(runs),
    }


strategies_to_test = [
    ("Only Random Walker", "only_random_walker", OnlyRandomWalkerStrategyParams()),
    (
        "Only Random Walker (with Memory)",
        "only_random_walker",
        OnlyRandomWalkerStrategyParams(100),
    ),
    (
        "Random Walker 1",
        "random_walker_1",
        RandomWalker1StrategyParams(0.82, 0.01, 100),
    ),
    (
        "Random Walker 2 (OnlySearchedInformation)",
        "random_walker_2",
        RandomWalker2StrategyParams(0.82, 100, "OnlySearchedInformation"),
    ),
    (
        "Random Walker 2 (EveryXStepsLowestDistanceToSearchedInformation)",
        "random_walker_2",
        RandomWalker2StrategyParams(
            0.82, 100, "EveryXStepsLowestDistanceToSearchedInformation"
        ),
    ),
    (
        "Random Walker 2 (EveryXStepsHighestDistanceToSearchedInformation)",
        "random_walker_2",
        RandomWalker2StrategyParams(
            0.82, 100, "EveryXStepsHighestDistanceToSearchedInformation"
        ),
    ),
    (
        "Random Walker 2 (EveryXStepsToNearestToCurrentInformation)",
        "random_walker_2",
        RandomWalker2StrategyParams(
            0.82, 100, "EveryXStepsToNearestToCurrentInformation"
        ),
    ),
    (
        "Random Walker 2 (EveryXStepsRandomConnection)",
        "random_walker_2",
        RandomWalker2StrategyParams(0.82, 100, "EveryXStepsRandomConnection"),
    ),
    (
        "Random Walker 2 (EveryRandomStepsNearestToCurrentInformation)",
        "random_walker_2",
        RandomWalker2StrategyParams(
            0.82, 100, "EveryRandomStepsNearestToCurrentInformation",  (1.0 / 50.0),
        ),
    ),
    (
        "Random Walker 2 (EveryRandomStepsLowestDistanceToSearchedInformation)",
        "random_walker_2",
        RandomWalker2StrategyParams(
            0.82, 100, "EveryRandomStepsLowestDistanceToSearchedInformation", (1.0 / 50)
        ),
    ),
    
]

# ToDo: 
# Increasing Probability?

results_for_strategies = []

for strategy in strategies_to_test:
    print(f"Testing strategy {strategy[0]}")

    # Measure time
    strategy_start_time = time.time()

    # simulate 20 times and show averages
    runs = []

    def _run(index):
        loguru.logger.remove()
        loguru.logger.add("strategy_comparator.log", level="ERROR")

        print(f"Run {index}")

        # Measure time
        start_time = time.time()

        res = simulate(
            graph_strategy="random",
            graph_stratey_params=RandomStrategyParams(),
            grid_width=200,
            grid_height=300,
            num_distinct_information=100,
            random_walker_strategy=strategy[1],
            random_walker_strategy_params=strategy[2],
            num_random_walker=10,
            searched_information=50,
            max_steps=500000,
            random_walker_start_point_strategy="RandomNode",
        )

        print(f"Run {index} took {time.time() - start_time} seconds")

        return res


    #runs = [_run() for i in range(100)]
    # run in parallel joblib

    runs = Parallel(n_jobs=4, batch_size=5)(delayed(_run)(i) for i in range(100))

    results_for_strategies.append(print_for_result(strategy[0], runs))#

    print(f"Testing strategy {strategy[0]} took {time.time() - strategy_start_time} seconds")

# create dataframe
df = pd.DataFrame(results_for_strategies)

# display dataframe as html to file and open in browser
# highligh column num_steps_avg
html = df.style.highlight_min(subset=["num_steps_avg"]).to_html()
with open("strategy_comparator.html", "w") as f:
    f.write(html)

# import webbrowser

# webbrowser.open("strategy_comparator.html")
