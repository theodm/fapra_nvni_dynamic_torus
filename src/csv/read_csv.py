import csv

from dataclasses import dataclass
import random
from statistics import stdev
from typing import Literal

from src.search.simulation import simulate
from src.search.strategy.only_random_walker import OnlyRandomWalkerStrategyParams
from src.search.strategy.random_walker_1 import RandomWalker1StrategyParams
from src.search.strategy.random_walker_2 import RandomWalker2StrategyParams
from src.torus_creation.random_grid import RandomNormalStrategyParams, RandomStrategyParams

import pandas as pd

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
        "anzahl_schritte",
        "group",
        "normal_mean",
        "normal_std_dev"
    ]
)

def read_csv_and_execute(file, fn):
    icsv = csv.reader(open(file, "r"))

    # skip header
    next(icsv)
    
    for row in icsv:
        params = ExecutionParams(
            seed = int(row[2]),
            erstellungsmethode = row[3], # type: ignore
            width = int(row[4]),
            height = int(row[5]),
            anzahl_informationen = int(row[6]),
            anzahl_walker = int(row[7]),
            startpunkte = eval(row[8]),
            gesuchte_information_num = int(row[13]),
            normal_mean = float(row[17]),
            normal_std_dev = float(row[18]),
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
        ])

def execute(params: ExecutionParams):
    random.seed(params.seed)

    graph_strategy = params.erstellungsmethode
    graph_strategy_params = graph_strategy == "random" and RandomStrategyParams() or RandomNormalStrategyParams(
        mean=params.normal_mean,
        std_dev=params.normal_std_dev
    )

    res = simulate(
        graph_strategy="random",
        graph_stratey_params=RandomStrategyParams(),
        grid_width=40,
        grid_height=40,
        num_distinct_information=100,
        random_walker_strategy=strategy[1],
        random_walker_strategy_params=strategy[2],
        num_random_walker=10,
        searched_information=50,
        max_steps=3000,
        random_walker_start_point_strategy="RandomNode",
    )


read_csv_and_execute(
    "data.csv",

)