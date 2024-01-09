from cgitb import small
from dataclasses import dataclass

import networkx
import random
from src.torus_creation.random_grid_shared import sh_create_random_2d_grid_network, sh_create_random_normal_2d_grid_network

from src.torus_creation.shared.torus_utils import map_2d_point_to_3d_torus
import scipy.stats as stats
from loguru import logger


@dataclass
class RandomStrategyParams:
    small_world: bool = False
    pass


@dataclass
class RandomNormalStrategyParams:
    mean: float
    std_dev: float
    small_world: bool = False

    @staticmethod
    def default(num_distinct_information: int, small_world: bool = False):
        return RandomNormalStrategyParams(
            mean=num_distinct_information / 2 - 1,
            std_dev=num_distinct_information / 8,
            small_world=small_world,
        )

    pass


def create_random_2d_grid_network_normal_with_params(
    width: int,
    height: int,
    num_distinct_information: int,
    params: RandomNormalStrategyParams,
) -> networkx.Graph:
    return create_random_2d_grid_network_normal(
        width=width,
        height=height,
        num_distinct_information=num_distinct_information,
        mean=params.mean,
        std_dev=params.std_dev,
    )


def create_random_2d_grid_network_normal(
    width: int,
    height: int,
    num_distinct_information: int,
    mean: float,
    std_dev: float,
    small_world: bool = False
) -> networkx.Graph:
    g = sh_create_random_normal_2d_grid_network(
        width=width,
        height=height,
        num_distinct_information=num_distinct_information,
        mean=mean,
        std_dev=std_dev,
        small_world=small_world,
    )    

    _add_3d_pos_to_graph(g, width, height)

    return g


def create_random_2d_grid_network_with_params(
    width: int,
    height: int,
    num_distinct_information: int,
    params: RandomStrategyParams,
) -> networkx.Graph:
    return create_random_2d_grid_network(
        width=width,
        height=height,
        num_distinct_information=num_distinct_information,
    )


def create_random_2d_grid_network(
    width: int,
    height: int, 
    num_distinct_information: int,
    small_world: bool = False
) -> networkx.Graph:
    g = sh_create_random_2d_grid_network(
        width=width,
        height=height,
        num_distinct_information=num_distinct_information,
        small_world=small_world,
    )    

    _add_3d_pos_to_graph(g, width, height)

    return g

def _add_3d_pos_to_graph(g: networkx.Graph, width: int, height: int):
    for node in g.nodes():
        t_pos = map_2d_point_to_3d_torus(node[0], node[1], width, height)

        # 3D-Koordinaten des Knotens
        g.nodes[node]["x_pos"] = t_pos[0]
        g.nodes[node]["y_pos"] = t_pos[1]
        g.nodes[node]["z_pos"] = t_pos[2]
    
    return g