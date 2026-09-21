import matplotlib.patches as patches
import matplotlib.pyplot as plt
from neat import DefaultGenome
from pprint import pprint


def visualize_genome(genome:DefaultGenome, input_node_names, output_node_names):
    print(genome.nodes)
    pass

if __name__ == "__main__":
    from neat_playground.managers.scenario_runner_manager import ScenarioRunnerManager
    from neat_playground.data.scenario import Scenario
    manager = ScenarioRunnerManager()
    test_scenario = Scenario("src/neat_playground/scenarios/test_scenario")
    winner, winner_net = manager.run_scenario(test_scenario)
    #print("WINNER: \n", winner)
    #print("WINNER NET: \n", winner_net)

    #print("began for loop")
    # for key in winner.nodes:
    #     print(f"Key: {key}. Value: {winner.nodes[key]}")
    #     pprint(vars(winner.nodes[key]))

    #pprint(vars(winner_net))

    input_node_keys = dict()
    output_node_keys = dict()

    input_node_keys_sum = 0
    output_node_keys_sum = 0

    def assign_input_or_output_dict(key, current_input_sum, current_output_sum):
        input_sum = current_input_sum
        output_sum = current_output_sum
        if key < 0:
            if key not in input_node_keys:
                input_node_keys[key] = (-1, 0)
                input_sum += abs(key)
        else:
            if key not in output_node_keys:
                output_node_keys[key] = (1, 0)
                output_sum += abs(key)

        return input_sum, output_sum
            
    # Get all the keys and sort them into the appropriate dictionary.
    for connection in winner.connections.values():
        from_connection, to_connection = connection.key
        input_node_keys_sum, output_node_keys_sum = assign_input_or_output_dict(from_connection, input_node_keys_sum, output_node_keys_sum)
        input_node_keys_sum, output_node_keys_sum = assign_input_or_output_dict(to_connection, input_node_keys_sum, output_node_keys_sum)

    # Calculate Y position/Scaling and update dictionary tuple.
    scaling = 25
    minx, miny, maxx, maxy = 0, 0, 0, 0
    index = 0
    input_length = len(input_node_keys)-1
    output_length = len(output_node_keys)-1
    largest_length = max(input_length, output_length)

    for key in input_node_keys:
        currentX, currentY = input_node_keys[key]
        yVal = index / input_length - 0.5
        newX, newY = currentX * scaling, yVal * scaling
        input_node_keys[key] = (newX, newY)
        if newX < minx:
            minx = newX
        if newX > maxx:
            maxx = newX
        if newY < miny:
            miny = newY
        if newY > maxy:
            maxy = newY
        index += 1

    index = 0
    for key in output_node_keys:
        currentX, currentY = output_node_keys[key]
        yVal = index / output_length - 0.5
        newX, newY = currentX * scaling, yVal * scaling
        output_node_keys[key] = (newX, newY)
        if newX < minx:
            minx = newX
        if newX > maxx:
            maxx = newX
        if newY < miny:
            miny = newY
        if newY > maxy:
            maxy = newY
        index += 1

    # Draw the nodes on the graph.
    fig, ax = plt.subplots()

    for key in input_node_keys:
        circle = patches.Circle(
            input_node_keys[key], 1, label=f"{key}"
        )
        ax.add_patch(circle)
        x, y = input_node_keys[key]
        ax.text(x, y, f"{key}", fontsize=12, fontweight='bold', ha='center', va='center')

    for key in output_node_keys:
        circle = patches.Circle(
            output_node_keys[key], 1, label=f"{key}"
        )
        ax.add_patch(circle)
        x, y = output_node_keys[key]
        ax.text(x, y, f"{key}", fontsize=12, fontweight='bold', ha='center', va='center')

    merged = input_node_keys | output_node_keys
    for connection in winner.connections.values():
        from_connection, to_connection = connection.key
        x1, y1 = merged[from_connection]
        x2, y2 = merged[to_connection]
        ax.plot([x1, x2], [y1, y2], 'go-', linewidth=connection.weight*2)
        #midx = (x2 - x1)/2
        #midy = (y2 - y2)/2
        #ax.text(midx, midy, f"{connection.weight:.2f}", fontsize=12, fontweight='bold', ha='center', va='center')
    #ax.plot([minx, maxx], [miny, maxy], 'go-', linewidth=2)
    ax.set_aspect("equal")

    
    padding = 2
    ax.set_xlim(minx - padding, maxx + padding)
    ax.set_ylim(miny - padding, maxy + padding)

    plt.show()

    