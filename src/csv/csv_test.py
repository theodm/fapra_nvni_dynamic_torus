from src.csv.read_csv import ExecutionParams, ExecutionResult, read_csv_and_execute
from src.search.simulation import PredefinedNodeStartPointStrategy, simulate, PredefinedNodesStartPointStrategy
from src.search.strategy.only_random_walker import OnlyRandomWalkerStrategyParams
from src.search.strategy.random_walker_2 import RandomWalker2StrategyParams
from src.search.strategy.random_walker_3 import RandomWalker3StrategyParams
from src.torus_creation.random_grid import RandomStrategyParams, RandomNormalStrategyParams


def execute(params: ExecutionParams, random_walker_strategy, random_walker_strategy_params):
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
        random_walker_strategy=random_walker_strategy,
        random_walker_strategy_params=random_walker_strategy_params,
        num_random_walker=params.anzahl_walker,
        searched_information=params.gesuchte_information_num,
        max_steps=params.width * params.height * 20,
        random_walker_start_point_strategy=random_walker_start_point_strategy,
        graph_seed=params.seed,
    )

    if res["num_searched_nodes"] != params.test_check_num_nodes:
        print("ERROR: Wrong number of searched nodes " + str(res["num_searched_nodes"]) + " " + str(params.test_check_num_nodes))
        print(res)
        print(params)
        exit(1)

    return ExecutionResult(
        anzahl_schritte=res["num_steps"],
        anzahl_erstellter_kanten=res["edges_added"],
        runtime=res["convergence_time"]
    )

def dynamic_similar_0_5_0_0_200(params: ExecutionParams):
    return execute(params, "random_walker_3", RandomWalker3StrategyParams(
        random_probability=0.5,
        create_edge_strategy="dynamic_similar",
        random_probability_to_create_edge=0.0,
        length_of_memory=200,
    ))

def dynamic_similar_0_5_0_05_200(params: ExecutionParams):
    return execute(params, "random_walker_3", RandomWalker3StrategyParams(
        random_probability=0.5,
        create_edge_strategy="dynamic_similar",
        random_probability_to_create_edge=0.05,
        length_of_memory=200,
    ))

def dynamic_similar_0_5_0_1_200(params: ExecutionParams):
    return execute(params, "random_walker_3", RandomWalker3StrategyParams(
        random_probability=0.5,
        create_edge_strategy="dynamic_similar",
        random_probability_to_create_edge=0.1,
        length_of_memory=200,
    ))

def dynamic_random_0_5_0_0_200(params: ExecutionParams):
    return execute(params, "random_walker_3", RandomWalker3StrategyParams(
        random_probability=0.5,
        create_edge_strategy="dynamic_random",
        random_probability_to_create_edge=0.0,
        length_of_memory=200,
    ))

def dynamic_random_0_5_0_05_200(params: ExecutionParams):
    return execute(params, "random_walker_3", RandomWalker3StrategyParams(
        random_probability=0.5,
        create_edge_strategy="dynamic_random",
        random_probability_to_create_edge=0.05,
        length_of_memory=200,
    ))

def dynamic_random_0_5_0_1_200(params: ExecutionParams):
    return execute(params, "random_walker_3", RandomWalker3StrategyParams(
        random_probability=0.5,
        create_edge_strategy="dynamic_random",
        random_probability_to_create_edge=0.1,
        length_of_memory=200,
    ))

def random_memory_200(params: ExecutionParams):
    return execute(params, "only_random_walker", OnlyRandomWalkerStrategyParams(
        length_of_memory=200
    ))

read_csv_and_execute(
    "data_200.csv",
    "output/dynamic_similar_0.5_0.05_200.csv",
    dynamic_similar_0_5_0_05_200,
    parallel=True
)

read_csv_and_execute(
    "data_200.csv",
    "output/dynamic_random_0.5_0.05_200.csv",
    dynamic_random_0_5_0_05_200,
    parallel=True
)

read_csv_and_execute(
    "data_200.csv",
    "output/random_memory_200.csv",
    random_memory_200,
    parallel=True
)

read_csv_and_execute(
    "data_200.csv",
    "output2/dynamic_similar_0.5_0.0_200.csv",
    dynamic_similar_0_5_0_0_200,
    parallel=True
)

read_csv_and_execute(
    "data_200.csv",
    "output2/dynamic_random_0.5_0.0_200.csv",
    dynamic_random_0_5_0_0_200,
    parallel=True
)
#
# read_csv_and_execute(
#     "data_200.csv",
#     "output2/dynamic_similar_0.5_0.1_200.csv",
#     dynamic_similar_0_5_0_1_200,
#     parallel=True
# )
#
# read_csv_and_execute(
#     "data_200.csv",
#     "output2/dynamic_random_0.5_0.1_200.csv",
#     dynamic_random_0_5_0_1_200,
#     parallel=True
# )

