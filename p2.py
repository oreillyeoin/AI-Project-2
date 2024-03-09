import networkx as nx
import random
import matplotlib.pyplot as plt

def create_graph(graph_type, graph_params):
    if graph_type == "erdos_renyi":
        G = nx.erdos_renyi_graph(*graph_params)
    elif graph_type == "grid":
        G = nx.grid_2d_graph(*graph_params)
    elif graph_type == "watts_strogatz":
        G = nx.watts_strogatz_graph(*graph_params, p=0.2) 
    elif graph_type == "barabasi_albert":
        G = nx.barabasi_albert_graph(graph_params[0], m=graph_params[1]) 

    return G

def assign_colors(G, num_colors):
    color_assignment = {node: random.randint(1, num_colors) for node in G.nodes}
    return color_assignment


def visualize_graph(G, color_assignment):
    node_colors = [color_assignment[node] for node in G.nodes]
    nx.draw(G, with_labels=True, node_color=node_colors, cmap=plt.cm.rainbow)
    plt.show()


def count_conflicts(G, color_assignment):
    conflicts = [(u, v) for u, v in G.edges if color_assignment[u] == color_assignment[v]]
    return len(conflicts)


def get_node_with_max_conflicts(G, color_assignment):
    conflicts_per_node = {node: 0 for node in G.nodes}

    for u, v in G.edges:
        if color_assignment[u] == color_assignment[v]:
            conflicts_per_node[u] += 1
            conflicts_per_node[v] += 1

    max_conflicts = max(conflicts_per_node.values())
    nodes_with_max_conflicts = [node for node, conflicts in conflicts_per_node.items() if conflicts == max_conflicts]

    return random.choice(nodes_with_max_conflicts)


def color_conflict_resolution(G, color_assignment, num_colors, max_iterations=100):

    iteration = 1
    conflicts_count = count_conflicts(G, color_assignment)
    conflicts_over_time = [conflicts_count]
    best_conflicts_count = conflicts_count
    best_solution = color_assignment.copy()

    while iteration <= max_iterations:
        print(f"CN:{num_colors} | Iteration {iteration}: {conflicts_count} conflicts")

        if conflicts_count == 0:
            best_solution = color_assignment.copy()
            break  

        node_to_change = get_node_with_max_conflicts(G, color_assignment)
        old_color = color_assignment[node_to_change]

        available_colors = [color for color in range(1, num_colors + 1) if color != old_color]

        if available_colors:
            new_color = random.choice(available_colors)
            color_assignment[node_to_change] = new_color
            print(f"\t*Node {node_to_change} changed color from {old_color} to {new_color}")

        conflicts_count = count_conflicts(G, color_assignment)
        conflicts_over_time.append(conflicts_count)

        # Update the best solution if a lower conflicts count is found
        if conflicts_count < best_conflicts_count:
            best_conflicts_count = conflicts_count
            best_solution = color_assignment.copy()

        iteration += 1

    visualize_graph(G, best_solution)
    if best_conflicts_count != 0:
        print(f"\n[Lowest number of conflicts encountered: {best_conflicts_count} for CN: {num_colors}]\n")

    plt.plot(range(1, len(conflicts_over_time) + 1), conflicts_over_time, label=f"CN: {num_colors}")
    plt.xlabel("Iteration")
    plt.ylabel("Number of Conflicts")
    plt.legend()
    plt.show()

    return best_solution


def find_chromatic_number(G, max_colors):
    for num_colors in range(2, max_colors + 1):
        colors = assign_colors(G, num_colors)
        resolved_colors = color_conflict_resolution(G, colors, num_colors)

        if count_conflicts(G, resolved_colors) == 0:
            return num_colors

    print("Chromatic number not found within the specified range.")
    return None


if __name__ == "__main__":
    graph_types_to_try = ["erdos_renyi", "grid", "watts_strogatz", "barabasi_albert"]
    graph_params = {
        "erdos_renyi": (15, 0.3),
        "grid": (4, 4),
        "watts_strogatz": (15, 4), 
        "barabasi_albert": (15, 2) 
    }

    max_colors_to_try = 10

    for graph_type in graph_types_to_try:
        print(f"\n-------- Experimenting with {graph_type.capitalize()} Graph --------\n")
        graph = create_graph(graph_type, graph_params[graph_type])

        chromatic_number = find_chromatic_number(graph, max_colors_to_try)

        if chromatic_number is not None:
            print(f"\n---------SOLVED---------\n\nThe determined chromatic number for {graph_type.capitalize()} graph is: {chromatic_number}")
