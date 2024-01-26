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

# remove prefix output/ and suffix .csv from strategy
_ndf["strategy"] = _ndf["strategy"].str.replace("output/", "").str.replace(".csv", "")
# get all distinct values of the column "strategy"
print(_ndf["strategy"].unique())

res_data = []

# calculate result_anzahl_schritte mal anzah_walker (=num_messages)
_ndf["num_messages"] = _ndf["result_anzahl_schritte"] * _ndf["anzahl_walker"]

# filter groesse=200x300 and erstellungsmethode=random_normal and gesuchte_information=normal_selten
_ndf = _ndf[(_ndf["groesse"] == "200x300") & (_ndf["erstellungsmethode"] == "random_normal") & (_ndf["gesuchte_information"] == "normal_häufig")]

# group by anzahl_informationen and calculate mean for num_messages

datas = [
    # name
    # x
    # y
]

# for each strategy add data to datas
for strategy in _ndf["strategy"].unique():

    x = []
    y = []

    for anzahl_informationen in _ndf["anzahl_informationen"].unique():
        # get all rows with the current strategy, groesse, anzahl_walker and startpunkt
        _df = _ndf[
            (_ndf["strategy"] == strategy) &
            (_ndf["anzahl_informationen"] == anzahl_informationen)
        ]

        # get the average of the column "num_messages"
        avg = _df["num_messages"].mean()

        x.append("_" + str(anzahl_informationen))
        y.append(avg)

    datas.append({
        "name": strategy,
        "x": x,
        "y": y
    })


import plotly.graph_objects as go

plot = go.Figure(
    data=[
    go.Bar(
        name=data["name"],
        x=data["x"],
        y=data["y"]
    ) for data in datas
]
)
plot.update_layout(title_text='normalverteilt, seltene Information', xaxis_title_text='Anzahl der Informationen', yaxis_title_text='Anzahl der Nachrichten')

plot.show()

