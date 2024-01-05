from src.csv.read_csv import ExecutionParams, ExecutionResult, read_csv_and_execute
from src.search.simulation import PredefinedNodeStartPointStrategy, simulate, PredefinedNodesStartPointStrategy
from src.search.strategy.random_walker_2 import RandomWalker2StrategyParams
from src.torus_creation.random_grid import RandomStrategyParams, RandomNormalStrategyParams


def execute(params: ExecutionParams):
    graph_strategy = params.erstellungsmethode
    graph_strategy_params = RandomStrategyParams() if graph_strategy == "random" else RandomNormalStrategyParams(
        mean=params.normal_mean,
        std_dev=params.normal_std_dev
    )

    random_walker_start_point_strategy = PredefinedNodeStartPointStrategy(params.startpunkte[0]) if len(params.startpunkte) == 1 else PredefinedNodesStartPointStrategy(
        params.startpunkte
    )

    res = simulate(
        graph_strategy=graph_strategy,
        graph_stratey_params=graph_strategy_params,
        grid_width=params.width,
        grid_height=params.height,
        num_distinct_information=params.anzahl_informationen,
        random_walker_strategy="random_walker_2",
        random_walker_strategy_params=RandomWalker2StrategyParams(0.82, 100, "EveryXStepsRandomConnection"),
        num_random_walker=params.anzahl_walker,
        searched_information=params.gesuchte_information_num,
        max_steps=params.width * params.height * 10,
        random_walker_start_point_strategy=random_walker_start_point_strategy,
        graph_seed=params.seed,
    )

    if res["num_searched_nodes"] != params.test_check_num_nodes:
        print("ERROR: Wrong number of searched nodes " + str(res["num_searched_nodes"]) + " " + str(params.test_check_num_nodes))
        print(res)
        print(params)
        exit(1)

    return ExecutionResult(
        anzahl_schritte=res["num_steps"]
    )

read_csv_and_execute(
    "data.csv",
    "output/rw2.csv",
    execute,
    parallel=True
)