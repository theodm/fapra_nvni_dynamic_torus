import csv

from dataclasses import dataclass
import random
from statistics import stdev
from typing import Literal

from src.search.simulation import simulate, PredefinedNodesStartPointStrategy, PredefinedNodeStartPointStrategy
from src.search.strategy.only_random_walker import OnlyRandomWalkerStrategyParams
from src.search.strategy.random_walker_1 import RandomWalker1StrategyParams
from src.search.strategy.random_walker_2 import RandomWalker2StrategyParams
from src.torus_creation.random_grid import RandomNormalStrategyParams, RandomStrategyParams

import pandas as pd

# disable loguru
import loguru

loguru.logger.remove()

@dataclass
class ExecutionParams:
    seed: int

    erstellungsmethode: Literal["random"] | Literal["random_normal"]
    width: int
    height: int
    anzahl_informationen: int
    anzahl_walker: int
    startpunkte: tuple | list[tuple]
    gesuchte_information_num: int

    test_check_num_nodes: int

    normal_mean: float = 0
    normal_std_dev: float = 0

@dataclass
class ExecutionResult:
    anzahl_schritte: int

output_csv = csv.writer(open("output_data.csv", "w"))

# write header
output_csv.writerow(
    [
        "result_anzahl_schritte",
        "id",
        "execution_num",
        "seed",
        "erstellungsmethode",
        "groesse",
        "d_groesse_width",
        "d_groesse_height",
        "anzahl_informationen",
        "anzahl_walker",
        "startpunkt",
        "startpunkte",
        "anzahl_simulationen",
        "gesuchte_information",
        "gesuchte_information_num",
        "group",
        "normal_mean",
        "normal_std_dev",
        "test_check_num_nodes"
    ]
)

def read_csv_and_execute(file, fn):
    icsv = csv.reader(open(file, "r"))

    # skip header
    next(icsv)

    executions = []

    for row in icsv:
        # access rows by name
        params = ExecutionParams(
            seed=int(row[2]),
            erstellungsmethode=row[3],
            width=int(row[5]),
            height=int(row[6]),
            anzahl_informationen=int(row[7]),
            anzahl_walker=int(row[8]),
            startpunkte=eval(row[10]),
            gesuchte_information_num=int(row[13]),
            test_check_num_nodes=int(row[17]),
            normal_mean=float(row[15]) if row[15] != "" else 0.0,
            normal_std_dev=float(row[16]) if row[16] != "" else 0.0,
        )

        result = fn(params)

        output_csv.writerow([
            result.anzahl_schritte,
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
            row[6],
            row[7],
            row[8],
            row[9],
            row[10],
            row[11],
            row[12],
            row[13],
            row[14],
            row[15],
            row[16],
            row[17],
        ])

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
    execute
)