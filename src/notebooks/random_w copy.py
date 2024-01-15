
from src.plot.draw_torus import ColorModeNumberOfTimesVisited, SizeModeNone, draw_torus_2d
from src.search.simulation import PredefinedNodesStartPointStrategy, RandomNodeStartPointStrategy, SingleRandomNodeStartPointStrategy, simulate
from src.search.strategy.only_random_walker import OnlyRandomWalkerStrategyParams
from src.torus_creation.random_grid import RandomStrategyParams

from joblib import Parallel, delayed

# disable loguru
import loguru
loguru.logger.remove()

j_to_avg = {}
sim_sim_results = {}

def simulate_wrapper(j):
    # disable loguru
    import loguru
    loguru.logger.remove()
    sim_results = []
    for i in range(0, 500):
        res = simulate(
            graph_strategy="random",
            graph_stratey_params=RandomStrategyParams(),
            grid_width=100,
            grid_height=100,
            num_distinct_information=100,
            random_walker_strategy="only_random_walker",
            random_walker_strategy_params=OnlyRandomWalkerStrategyParams(j),
            num_random_walker=5,
            searched_information=50,
            max_steps=100000,
            random_walker_start_point_strategy=RandomNodeStartPointStrategy(),
        )
        
        print(f"-- {j} {i} {res['num_steps']}")

        sim_results.append(res["num_steps"])

    return sim_results

results = Parallel(n_jobs=-1)(delayed(simulate_wrapper)(j) for j in range(1, 300))

for j, sim_results in enumerate(results, start=1):
    print(f"{j} {sum(sim_results)/len(sim_results)}")
    j_to_avg[j] = sum(sim_results)/len(sim_results)
    sim_sim_results[j] = sim_results
    

# write to file as json
import json
with open('j_to_avg.json', 'w') as fp:
    json.dump(j_to_avg, fp)
with open('sim_sim_results.json', 'w') as fp:
    json.dump(sim_sim_results, fp)


    