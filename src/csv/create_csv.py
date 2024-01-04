
from src.torus_creation.random_grid import create_random_2d_grid_network, create_random_2d_grid_network_normal
import csv 
import random
import sys
import hashlib

# disable loguru
import loguru
loguru.logger.remove()

# Parameter
#
# Breite x Höhe = 100x100 oder 200x300
# Torus-Erstellungsmethode = "random" oder "random_normal"
# Anzahl unterschiedlicher Informationen = 10 oder 100 oder 1000
# 
# Anzahl Walker = 1 oder 10 oder 100
# Gesuchte Information = "normal_selten" oder "normal_mittel" oder "normal_häufig"
# Startpunkt der Random Walker = "same" oder "random_each"
#
# Anzahl an Simulationen = 100 oder 500 oder 1000
#

erstellungsmethode = ["random_normal", "random"]

groesse = ["100x100", "200x300"]
anzahl_informationen = [10, 100, 1000]
anzahl_walker = [1, 10, 100]
startpunkt = ["same", "random_each"]
anzahl_simulationen = [1] #[200]

gesuchte_information_normal = ["normal_selten", "normal_mittel", "normal_häufig"]
gesuchte_information_random = ["<not defined>"]

# create output csv file and delete old one
csv = csv.writer(open("data.csv", "w"))

# write header
csv.writerow(
    [
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
        "normal_std_dev"

    ]
)
count = 0

for e in erstellungsmethode:
    for g in groesse:
        for i in anzahl_informationen:
            for w in anzahl_walker:
                for s in startpunkt:
                    for a in anzahl_simulationen:
                        for gi in (gesuchte_information_normal if e == "random_normal" else gesuchte_information_random):
                            for _ in range(a):
                                count += 1

used_seeds = []

c = 0
for e in erstellungsmethode:
    for g in groesse:
        for i in anzahl_informationen:
            for w in anzahl_walker:
                for s in startpunkt:
                    for a in anzahl_simulationen:
                        for gi in (gesuchte_information_normal if e == "random_normal" else gesuchte_information_random):
                            for _ in range(a):
                                c = c + 1
                                # generate random seed (max int)
                                while True:
                                    seed = random.randint(0, sys.maxsize)
                                    if seed not in used_seeds:
                                        used_seeds.append(id)
                                        break
                                
                                num_distinct_information = i

                                width = int(g.split("x")[0])
                                height = int(g.split("x")[1])

                                # seed setzen
                                random.seed(seed)
                                
                                mean = None
                                std_dev = None

                                # erstelle den graphen für den seed
                                if e == "random":
                                    graph = create_random_2d_grid_network(
                                        width=width,
                                        height=height,
                                        num_distinct_information=num_distinct_information    
                                    )

                                    gesuchte_information_num = random.randrange(0, num_distinct_information)
                                elif e == "random_normal":
                                    mean = num_distinct_information / 2 - 1
                                    std_dev = num_distinct_information / 8

                                    graph = create_random_2d_grid_network_normal(
                                        width=width,
                                        height=height,
                                        num_distinct_information=num_distinct_information,
                                        mean=mean,
                                        std_dev=std_dev,
                                    )
                                    
                                    # wir erstellen eine Verteilung der im Graph vorkommenden Informationen
                                    # und wählen dann eine Information die selten, mittel oder häufig vorkommt
                                    verteilung = [0] * num_distinct_information
                                    for node in graph.nodes:
                                        verteilung[graph.nodes[node]["information"]] += 1
                                    
                                    verteilung_to_information = [
                                        (verteilung[x], x) for x in range(num_distinct_information)
                                    ]

                                    # sortiere nach häufigkeit absteigend
                                    verteilung_to_information.sort(key=lambda x: x[0], reverse=True)

                                    drittel = len(verteilung_to_information) // 3
                                    if gi == "normal_selten":
                                        bb = verteilung_to_information[:drittel]
                                        bb = [x for x in bb if x[0] > 0]
                                        gesuchte_information_num = random.choice(bb)[0]
                                    elif gi == "normal_mittel":
                                        bb = verteilung_to_information[drittel:2 * drittel]
                                        bb = [x for x in bb if x[0] > 0]
                                        gesuchte_information_num = random.choice(bb)[0]
                                    elif gi == "normal_häufig":
                                        bb = verteilung_to_information[2 * drittel:]
                                        bb = [x for x in bb if x[0] > 0]
                                        gesuchte_information_num = random.choice(bb)[0]
                                else:
                                    raise Exception("Erstellungsmethode nicht bekannt")
                                
                                startpunkte = []

                                if s == "same":
                                    # select random node
                                    random_node = random.choice(list(graph.nodes))

                                    startpunkte = random_node
                                elif s == "random_each":
                                    for _ in range(w):
                                        # select random node
                                        random_node = random.choice(list(graph.nodes))

                                        startpunkte.append(random_node)
                                    
                                # id is hash of parameters
                                id = hashlib.sha256(
                                    str(
                                        (
                                            e,
                                            g,
                                            i,
                                            w,
                                            s,
                                            a,
                                            gi,
                                            _,
                                            seed,
                                            gesuchte_information_num,
                                            str(startpunkte)
                                        )
                                    ).encode("utf-8")
                                ).hexdigest()
                                
                                group = f"{e}_{g}_{i}_{w}_{s}_{gi}"

                                row =  [
                                        # id
                                        id,
                                        # execution_num
                                        _,
                                        # seed
                                        seed,
                                        # erstellungsmethode
                                        e, 
                                        # groesse
                                        g,
                                        # groesse_width
                                        g.split("x")[0],
                                        # groesse_height
                                        g.split("x")[1],
                                        # anzahl_informationen
                                        i, 
                                        # anzahl_walker
                                        w, 
                                        # startpunkt
                                        s,
                                        # startpunkte
                                        str(startpunkte),
                                        # anzahl_simulationen
                                        a,
                                        # gesuchte_information
                                        gi,
                                        # gesuchte_information_num
                                        gesuchte_information_num,
                                        # group
                                        group,
                                        # normal_mean
                                        mean,
                                        # normal_std_dev
                                        std_dev,
                                    ]

                                #print(row)
                                
                                if c % 100 == 0:
                                    print(f"{c} / {count}")

                                csv.writerow(
                                   row
                                )
