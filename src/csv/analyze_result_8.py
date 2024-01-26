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


# scatter plot with plotly
# test_check_num_nodes on x axis and y axis is num_messages

import plotly.express as px

fig = px.scatter(_ndf, x="test_check_num_nodes", y="num_messages", color="strategy")

fig.show()


# group by startpunkt
#
# _ndf = _ndf.groupby(["startpunkt", "strategy", "groesse", "anzahl_walker"])
#
# print(_ndf)