from statistics import stdev
from src.search.simulation import plot_single_result, simulate
from src.search.strategy.only_random_walker import OnlyRandomWalkerStrategyParams
from src.search.strategy.random_walker_1 import RandomWalker1StrategyParams

# simulate 20 times and show averages
resultsB = []
for i in range(1500):
    res = simulate(
        graph_strategy="random",
        grid_width=40,
        grid_height=40,
        num_distinct_information=100,
        random_walker_strategy="only_random_walker",
        random_walker_strategy_params=OnlyRandomWalkerStrategyParams(
        ),
        num_random_walker=10,
        searched_information=50,
        max_steps=3000,
    )

    resultsB.append(res)

# simulate 20 times and show averages
resultsA = []
for i in range(1500):
    res = simulate(
        graph_strategy="random",
        grid_width=40,
        grid_height=40,
        num_distinct_information=100,
        random_walker_strategy="random_walker_1",
        random_walker_strategy_params=RandomWalker1StrategyParams(
            random_probability=0.9,
            random_probability_of_adding_edge=0.005,
            length_of_memory=150,
        ),
        num_random_walker=10,
        searched_information=50,
        max_steps=3000,
    )

    resultsA.append(res)

def print_info_for_attribute(objs, attribute_name):
    print("attribute_name: ", attribute_name)
    avg = sum([r[attribute_name] for r in objs]) / len(objs)
    _min = min([r[attribute_name] for r in objs])
    _max = max([r[attribute_name] for r in objs])
    std_dev = stdev([r[attribute_name] for r in objs])

    print(f"avg: {avg}")
    print(f"min: {_min}")
    print(f"max: {_max}")
    print(f"std_dev: {std_dev}")
    print(f"")

def print_for_result(objs):
    print_info_for_attribute(objs, "num_steps")
    print_info_for_attribute(objs, "num_found_nodes")
    print_info_for_attribute(objs, "num_searched_nodes")

    num_times_out_of_steps = sum([(0 if r["break_type"] == "all_found" else 1) for r in objs]) 
    num_times = len(objs)

    print(f"num_times_out_of_steps: {num_times_out_of_steps}")
    print(f"num_times: {num_times}")
    print(f"")

print("A")
print_for_result(resultsA)
print("B")
print_for_result(resultsB)

# Results:
# A
# attribute_name:  num_steps
# avg: 1191.794
# min: 234
# max: 3000
# std_dev: 479.88461431824726

# attribute_name:  num_found_nodes
# avg: 16.014
# min: 5
# max: 29
# std_dev: 3.9217416247862444

# attribute_name:  num_searched_nodes
# avg: 16.018666666666668
# min: 5
# max: 29
# std_dev: 3.923847934187729

# num_times_out_of_steps: 7
# num_times: 1500

# B
# attribute_name:  num_steps
# avg: 1301.876
# min: 191
# max: 3000
# std_dev: 491.5528762104241

# attribute_name:  num_found_nodes
# avg: 16.066
# min: 5
# max: 30
# std_dev: 3.939711269021564

# attribute_name:  num_searched_nodes
# avg: 16.07133333333333
# min: 5
# max: 30
# std_dev: 3.9394489116339364

# num_times_out_of_steps: 8
# num_times: 1500