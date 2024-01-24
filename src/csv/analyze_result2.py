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

groups = [
    "random_100x100_1000_100_random_each_<not defined>",
    "random_100x100_1000_100_same_<not defined>",
    "random_100x100_1000_10_random_each_<not defined>",
    "random_100x100_1000_10_same_<not defined>",
    "random_100x100_1000_1_random_each_<not defined>",
    "random_100x100_1000_1_same_<not defined>",
    "random_100x100_100_100_random_each_<not defined>",
    "random_100x100_100_100_same_<not defined>",
    "random_100x100_100_10_random_each_<not defined>",
    "random_100x100_100_10_same_<not defined>",
    "random_100x100_100_1_random_each_<not defined>",
    "random_100x100_100_1_same_<not defined>",
    "random_100x100_10_100_random_each_<not defined>",
    "random_100x100_10_100_same_<not defined>",
    "random_100x100_10_10_random_each_<not defined>",
    "random_100x100_10_10_same_<not defined>",
    "random_100x100_10_1_random_each_<not defined>",
    "random_100x100_10_1_same_<not defined>",
    # "random_200x300_1000_100_random_each_<not defined>",
    # "random_200x300_1000_100_same_<not defined>",
    # "random_200x300_1000_10_random_each_<not defined>",
    # "random_200x300_1000_10_same_<not defined>",
    # "random_200x300_1000_1_random_each_<not defined>",
    # "random_200x300_1000_1_same_<not defined>",
    # "random_200x300_100_100_random_each_<not defined>",
    # "random_200x300_100_100_same_<not defined>",
    # "random_200x300_100_10_random_each_<not defined>",
    # "random_200x300_100_10_same_<not defined>",
    # "random_200x300_100_1_random_each_<not defined>",
    # "random_200x300_100_1_same_<not defined>",
    # "random_200x300_10_100_random_each_<not defined>",
    # "random_200x300_10_100_same_<not defined>",
    # "random_200x300_10_10_random_each_<not defined>",
    # "random_200x300_10_10_same_<not defined>",
    # "random_200x300_10_1_random_each_<not defined>",
    # "random_200x300_10_1_same_<not defined>",
    "random_normal_100x100_1000_100_random_each_normal_häufig",
    "random_normal_100x100_1000_100_random_each_normal_mittel",
    "random_normal_100x100_1000_100_random_each_normal_selten",
    "random_normal_100x100_1000_100_same_normal_häufig",
    "random_normal_100x100_1000_100_same_normal_mittel",
    "random_normal_100x100_1000_100_same_normal_selten",
    "random_normal_100x100_1000_10_random_each_normal_häufig",
    "random_normal_100x100_1000_10_random_each_normal_mittel",
    "random_normal_100x100_1000_10_random_each_normal_selten",
    "random_normal_100x100_1000_10_same_normal_häufig",
    "random_normal_100x100_1000_10_same_normal_mittel",
    "random_normal_100x100_1000_10_same_normal_selten",
    "random_normal_100x100_1000_1_random_each_normal_häufig",
    "random_normal_100x100_1000_1_random_each_normal_mittel",
    "random_normal_100x100_1000_1_random_each_normal_selten",
    "random_normal_100x100_1000_1_same_normal_häufig",
    "random_normal_100x100_1000_1_same_normal_mittel",
    "random_normal_100x100_1000_1_same_normal_selten",
    "random_normal_100x100_100_100_random_each_normal_häufig",
    "random_normal_100x100_100_100_random_each_normal_mittel",
    "random_normal_100x100_100_100_random_each_normal_selten",
    "random_normal_100x100_100_100_same_normal_häufig",
    "random_normal_100x100_100_100_same_normal_mittel",
    "random_normal_100x100_100_100_same_normal_selten",
    "random_normal_100x100_100_10_random_each_normal_häufig",
    "random_normal_100x100_100_10_random_each_normal_mittel",
    "random_normal_100x100_100_10_random_each_normal_selten",
    "random_normal_100x100_100_10_same_normal_häufig",
    "random_normal_100x100_100_10_same_normal_mittel",
    "random_normal_100x100_100_10_same_normal_selten",
    "random_normal_100x100_100_1_random_each_normal_häufig",
    "random_normal_100x100_100_1_random_each_normal_mittel",
    "random_normal_100x100_100_1_random_each_normal_selten",
    "random_normal_100x100_100_1_same_normal_häufig",
    "random_normal_100x100_100_1_same_normal_mittel",
    "random_normal_100x100_100_1_same_normal_selten",
    "random_normal_100x100_10_100_random_each_normal_häufig",
    "random_normal_100x100_10_100_random_each_normal_mittel",
    "random_normal_100x100_10_100_random_each_normal_selten",
    "random_normal_100x100_10_100_same_normal_häufig",
    "random_normal_100x100_10_100_same_normal_mittel",
    "random_normal_100x100_10_100_same_normal_selten",
    "random_normal_100x100_10_10_random_each_normal_häufig",
    "random_normal_100x100_10_10_random_each_normal_mittel",
    "random_normal_100x100_10_10_random_each_normal_selten",
    "random_normal_100x100_10_10_same_normal_häufig",
    "random_normal_100x100_10_10_same_normal_mittel",
    "random_normal_100x100_10_10_same_normal_selten",
    "random_normal_100x100_10_1_random_each_normal_häufig",
    "random_normal_100x100_10_1_random_each_normal_mittel",
    "random_normal_100x100_10_1_random_each_normal_selten",
    "random_normal_100x100_10_1_same_normal_häufig",
    "random_normal_100x100_10_1_same_normal_mittel",
    "random_normal_100x100_10_1_same_normal_selten",
    # "random_normal_200x300_1000_100_random_each_normal_häufig",
    # "random_normal_200x300_1000_100_random_each_normal_mittel",
    # "random_normal_200x300_1000_100_random_each_normal_selten",
    # "random_normal_200x300_1000_100_same_normal_häufig",
    # "random_normal_200x300_1000_100_same_normal_mittel",
    # "random_normal_200x300_1000_100_same_normal_selten",
    # "random_normal_200x300_1000_10_random_each_normal_häufig",
    # "random_normal_200x300_1000_10_random_each_normal_mittel",
    # "random_normal_200x300_1000_10_random_each_normal_selten",
    # "random_normal_200x300_1000_10_same_normal_häufig",
    # "random_normal_200x300_1000_10_same_normal_mittel",
    # "random_normal_200x300_1000_10_same_normal_selten",
    # "random_normal_200x300_1000_1_random_each_normal_häufig",
    # "random_normal_200x300_1000_1_random_each_normal_mittel",
    # "random_normal_200x300_1000_1_random_each_normal_selten",
    # "random_normal_200x300_1000_1_same_normal_häufig",
    # "random_normal_200x300_1000_1_same_normal_mittel",
    # "random_normal_200x300_1000_1_same_normal_selten",
    # "random_normal_200x300_100_100_random_each_normal_häufig",
    # "random_normal_200x300_100_100_random_each_normal_mittel",
    # "random_normal_200x300_100_100_random_each_normal_selten",
    # "random_normal_200x300_100_100_same_normal_häufig",
    # "random_normal_200x300_100_100_same_normal_mittel",
    # "random_normal_200x300_100_100_same_normal_selten",
    # "random_normal_200x300_100_10_random_each_normal_häufig",
    # "random_normal_200x300_100_10_random_each_normal_mittel",
    # "random_normal_200x300_100_10_random_each_normal_selten",
    # "random_normal_200x300_100_10_same_normal_häufig",
    # "random_normal_200x300_100_10_same_normal_mittel",
    # "random_normal_200x300_100_10_same_normal_selten",
    # "random_normal_200x300_100_1_random_each_normal_häufig",
    # "random_normal_200x300_100_1_random_each_normal_mittel",
    # "random_normal_200x300_100_1_random_each_normal_selten",
    # "random_normal_200x300_100_1_same_normal_häufig",
    # "random_normal_200x300_100_1_same_normal_mittel",
    # "random_normal_200x300_100_1_same_normal_selten",
    # "random_normal_200x300_10_100_random_each_normal_häufig",
    # "random_normal_200x300_10_100_random_each_normal_mittel",
    # "random_normal_200x300_10_100_random_each_normal_selten",
    # "random_normal_200x300_10_100_same_normal_häufig",
    # "random_normal_200x300_10_100_same_normal_mittel",
    # "random_normal_200x300_10_100_same_normal_selten",
    # "random_normal_200x300_10_10_random_each_normal_häufig",
    # "random_normal_200x300_10_10_random_each_normal_mittel",
    # "random_normal_200x300_10_10_random_each_normal_selten",
    # "random_normal_200x300_10_10_same_normal_häufig",
    # "random_normal_200x300_10_10_same_normal_mittel",
    # "random_normal_200x300_10_10_same_normal_selten",
    # "random_normal_200x300_10_1_random_each_normal_häufig",
    # "random_normal_200x300_10_1_random_each_normal_mittel",
    # "random_normal_200x300_10_1_random_each_normal_selten",
    # "random_normal_200x300_10_1_same_normal_häufig",
    # "random_normal_200x300_10_1_same_normal_mittel",
    # "random_normal_200x300_10_1_same_normal_selten",
]

# filter by groups
ndf = _ndf[_ndf["group"].isin(groups)].sort_values(by=["group", "strategy"])

import plotly.express as px

fig = px.box(ndf, x="group", y="result_anzahl_schritte", color="strategy")
fig.show()