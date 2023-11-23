import networkx as networkx
import plotly.express as px


def plot_information_distribution(g: networkx.Graph, num_distinct_information: int):
    information_distribution = [0] * num_distinct_information

    for node in g.nodes():
        information_distribution[g.nodes[node]["information"]] += 1

    fig = px.bar(
        x=list(range(num_distinct_information)),
        y=information_distribution,
        labels={"x": "Information", "y": "Anzahl Knoten"},
    )

    fig.update_layout(
        bargap=0,
    )

    fig.show()
