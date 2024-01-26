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

# calculate result_anzahl_schritte mal anzah_walker (=num_messages)
_ndf["num_messages"] = _ndf["result_anzahl_schritte"] * _ndf["anzahl_walker"]

for strategy in _ndf["strategy"].unique():
    for erstellungsmethode in _ndf["erstellungsmethode"].unique():
        for groesse in _ndf["groesse"].unique():
            for gsi in _ndf["gesuchte_information"].unique():
                r = [
                    strategy,
                    groesse,
                    erstellungsmethode,
                    gsi
                ]

                for anzahl_informationen in _ndf["anzahl_informationen"].unique():
                    # get all rows with the current strategy, groesse, anzahl_walker and startpunkt
                    _df = _ndf[
                        (_ndf["strategy"] == strategy)
                        & (_ndf["groesse"] == groesse)
                        & (_ndf["erstellungsmethode"] == erstellungsmethode)
                        & (_ndf["anzahl_informationen"] == anzahl_informationen)
                        & (_ndf["gesuchte_information"] == gsi)
                    ]

                    # get the average of the column "result_anzahl_schritte"
                    avg = _df["num_messages"].mean()
                    avg_2 = _df["test_check_num_nodes"].mean()

                    r.append(avg)
                    r.append(avg_2)

                res_data.append(r)

# create a new dataframe with the result data
res_df = pd.DataFrame(
    res_data,
    columns=[
        "strategy",
        "groesse",
        "erstellungsmethode",
        "gesuchte_information",
        "avg_num_messages_10",
        "avg_num_messages_10_2",
        "avg_num_messages_100",
        "avg_num_messages_100_2",
        "avg_num_messages_1000",
        "avg_num_messages_1000_2",
    ]
)


# remove prefix output/ and suffix .csv from strategy
res_df["strategy"] = res_df["strategy"].str.replace("output/", "").str.replace(".csv", "")

#remove alle rows where avg_num_messages_10 is NaN
res_df = res_df.dropna(subset=["avg_num_messages_10"])

# incr_percentage from avg_num_messages_10 to avg_num_messages_100
res_df["incr_percentage_10_100"] = (
    res_df["avg_num_messages_100"]
    / res_df["avg_num_messages_10"]
    * 100 - 100
)

# incr_percentage from avg_num_messages_100 to avg_num_messages_1000
res_df["incr_percentage_100_1000"] = (
    res_df["avg_num_messages_1000"]
    / res_df["avg_num_messages_100"]
    * 100 - 100
)

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