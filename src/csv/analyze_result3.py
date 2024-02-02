# csv has following columns:
#
# "result_anzahl_schritte",
# "id",
# "execution_num",
# "seed",
# "erstellungsmethode",
# "groesse",
# "d_groesse_width",
# "d_groesse_height",
# "anzahl_informationen",
# "anzahl_walker",
# "startpunkt",
# "startpunkte",
# "anzahl_simulationen",
# "gesuchte_information",
# "gesuchte_information_num",
# "group",
# "normal_mean",
# "normal_std_dev",
# "test_check_num_nodes"
#

OUTPUT_FOLDER = "output"

# disable loguru
import loguru

loguru.logger.remove()

import os
import csv

# read all csv files in output folder
# and retrieve all executions of the csv files
# with the group "random_normal_200x300_100_100_same_normal_häufig"
# group them by csv file name

# enumarete all csv files in output folder
csv_files = []

for file in os.listdir(OUTPUT_FOLDER):
    if file.endswith(".csv"):
        csv_files.append(os.path.join(OUTPUT_FOLDER, file))

import pandas as pd

# group executions by csv file name and average the result_anzahl_schritte for each group
res = []

for csv_file in csv_files:
    df = pd.read_csv(csv_file)

    df["strategy"] = str(csv_file)

    res.append(df)

_ndf = pd.concat(res)

# get all distinct values of the column "strategy"
print(_ndf["strategy"].unique())

res_data = []

for strategy in _ndf["strategy"].unique():
    for groesse in _ndf["groesse"].unique():
        for anzahl_walker in _ndf["anzahl_walker"].unique():

            r = [
                strategy,
                groesse,
                anzahl_walker
            ]

            for startpunkt in ["random_each", "same"]:
                # get all rows with the current strategy, groesse, anzahl_walker and startpunkt
                _df = _ndf[
                    (_ndf["strategy"] == strategy)
                    & (_ndf["groesse"] == groesse)
                    & (_ndf["anzahl_walker"] == anzahl_walker)
                    & (_ndf["startpunkt"] == startpunkt)
                ]

                # get the average of the column "result_anzahl_schritte"
                avg = _df["result_anzahl_schritte"].mean()

                r.append(avg)

            res_data.append(r)

# create a new dataframe with the result data
res_df = pd.DataFrame(
    res_data,
    columns=[
        "strategy",
        "groesse",
        "anzahl_walker",
        "avg_result_anzahl_schritte_random_each",
        "avg_result_anzahl_schritte_same"
    ]
)

# add column "increase_prct" to dataframe which contains the percentage of increase of the column "avg_result_anzahl_schritte_same" compared to the column "avg_result_anzahl_schritte_random_each"
res_df["increase_prct"] = (
    res_df["avg_result_anzahl_schritte_random_each"]
    / res_df["avg_result_anzahl_schritte_same"]
    * 100 - 100
)

# remove prefix output/ and suffix .csv from strategy
res_df["strategy"] = res_df["strategy"].str.replace("output/", "").str.replace(".csv", "")


# round all values to 2 decimal places
res_df = res_df.round(2)

# # sort by groesse, anzahl_walker, then strategy
# res_df = res_df.sort_values(
#     by=[
#         "groesse",
#         "anzahl_walker",
#         "strategy"
#     ]
# )

print(res_df)


# group by startpunkt
#
# _ndf = _ndf.groupby(["startpunkt", "strategy", "groesse", "anzahl_walker"])
#
# print(_ndf)