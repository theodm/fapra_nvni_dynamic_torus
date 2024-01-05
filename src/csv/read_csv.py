import csv
import time

from dataclasses import dataclass
from typing import Literal

# disable loguru
import loguru
from joblib import Memory

loguru.logger.remove()

memory = Memory("cachedir", verbose=0)

@dataclass
class ExecutionParams:
    row_id: int
    group: str

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


def read_csv_and_execute(input_file, output_file, fn, parallel=False):
    global _num_rows

    @memory.cache
    def _fn(params: ExecutionParams) -> ExecutionResult:
        print(f"Executing row {params.row_id} of {_num_rows} ({params.group})")

        start_time = time.time()

        result = fn(params)

        elapsed_time = time.time() - start_time

        print(f"Finished row {params.row_id} of {_num_rows} in {elapsed_time} seconds")
        return result


    icsv = csv.reader(open(input_file, "r"))
    ocsv = csv.writer(open(output_file, "w"))

    # write header
    ocsv.writerow(
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

    # skip header
    next(icsv)

    executions = []

    i = 1
    for row in icsv:
        # access rows by name
        params = ExecutionParams(
            row_id=i,
            group=row[14],

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

        executions.append((row, params))
        i = i + 1

    _num_rows = i

    print("Executing " + str(len(executions)) + " rows")
    start_time = time.time()

    if not parallel:
        results = [(row, _fn(params)) for row, params in executions]
    else:
        # parallel with joblib
        from joblib import Parallel, delayed

        def __fn(row, params):
            return (row, _fn(params))

        results = Parallel(n_jobs=-1)(delayed(__fn)(row, params) for row, params in executions)

    print(f"Finished executing {len(executions)} rows in {time.time() - start_time} seconds")
    print ("Writing " + str(len(results)) + " rows")

    for (row, result) in results:
        ocsv.writerow([
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
