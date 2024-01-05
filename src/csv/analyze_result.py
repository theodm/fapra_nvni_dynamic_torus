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

    res.append((str(csv_file), df.groupby("group").mean("result_anzahl_schritte")))

# sort the groups by the average result_anzahl_schritte
res.sort(key=lambda x: x[1].values[0])

# print the sorted groups
for file_name, df in res:
    print(file_name)
    for d in df["result_anzahl_schritte"].items():
        print(str(d[0]) + " - " + str(d[1]))

    print("")




