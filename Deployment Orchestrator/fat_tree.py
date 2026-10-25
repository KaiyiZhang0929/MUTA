import networkx as nx
import matplotlib.pyplot as plt



def fat_device_list_to_path(G, in_device_list, out_device_list):
    P = {}
    path_idx = 0
    for i in in_device_list:
        for o in out_device_list:
            if i == o:
                continue
            for path in nx.all_simple_paths(G, source=i, target=o, cutoff=5):
                P[path_idx] = path
                path_idx += 1

    return P


def create_fat_tree_topology(k, in_device_list, out_device_list):
    Network_Topology = {}
    if k % 2 != 0:
        raise ValueError("k must be even.")

    G = nx.Graph()

    # Number of core, aggregation, and edge switches
    num_core = (k // 2) ** 2
    num_agg_per_pod = k // 2
    num_edge_per_pod = k // 2

    # Core switch nodes
    core_switches = list(range(num_core))
    G.add_nodes_from(core_switches, layer="core")

    # Pod structure
    agg_switches = []
    edge_switches = []
    for pod in range(k):
        # Aggregation and edge switches for this pod
        agg_switches_pod = [num_core + pod * num_agg_per_pod + i for i in range(num_agg_per_pod)]
        edge_switches_pod = [num_core + k * num_agg_per_pod + pod * num_edge_per_pod + i for i in range(num_edge_per_pod)]

        agg_switches.extend(agg_switches_pod)
        edge_switches.extend(edge_switches_pod)

        G.add_nodes_from(agg_switches_pod, layer="aggregation")
        G.add_nodes_from(edge_switches_pod, layer="edge")

        # Connect aggregation switches to core switches
        for agg_idx, agg_switch in enumerate(agg_switches_pod):
            for core_idx in range(agg_idx * (k // 2), (agg_idx + 1) * (k // 2)):
                G.add_edge(agg_switch, core_switches[core_idx])

        # Connect edge switches to aggregation switches
        for agg_switch in agg_switches_pod:
            for edge_switch in edge_switches_pod:
                G.add_edge(agg_switch, edge_switch)

    Network_Topology['Graph'] = G
    Network_Topology['Path'] = fat_device_list_to_path(G, in_device_list, out_device_list)
    Network_Topology['Device list'] = core_switches + agg_switches + edge_switches
    Network_Topology['num_core'] = num_core  # Save num_core for later use
    Network_Topology['num_agg_per_pod'] = num_agg_per_pod
    Network_Topology['num_edge_per_pod'] = num_edge_per_pod
    return Network_Topology

# # Generate and visualize a k-pod fat-tree topology
# k = 10
# in_device_list = [i for i in range(75, 120)]
# out_device_list = [120,121,122,123,124]
#
# fat_tree = create_fat_tree_topology(k, in_device_list, out_device_list)
#
# # Assign positions manually to place core switches at the top, aggregation in the middle, and edge switches at the bottom
# positions = {}
# layer_map = nx.get_node_attributes(fat_tree['Graph'], 'layer')
# num_core = fat_tree['num_core']
# num_agg_per_pod = fat_tree['num_agg_per_pod']
# num_edge_per_pod = fat_tree['num_edge_per_pod']
#
# # Define Y-coordinates for the layers
# y_core, y_agg, y_edge = 2, 1, 0
# x_spacing_core = 2  # Spacing for core switches
# x_spacing_pod = 10  # Spacing between pods
# x_spacing_within_pod = 2  # Spacing within a pod
#
# # Place nodes based on their layers
# for node, layer in layer_map.items():
#     if layer == "core":
#         idx = node
#         positions[node] = (idx * x_spacing_core, y_core)
#     elif layer == "aggregation":
#         pod = (node - num_core) // num_agg_per_pod
#         idx = (node - num_core) % num_agg_per_pod
#         positions[node] = (pod * x_spacing_pod + idx * x_spacing_within_pod, y_agg)
#     elif layer == "edge":
#         pod = (node - num_core - k * num_agg_per_pod) // num_edge_per_pod
#         idx = (node - num_core - k * num_agg_per_pod) % num_edge_per_pod
#         positions[node] = (pod * x_spacing_pod + idx * x_spacing_within_pod, y_edge)
#
# # Draw the topology
# plt.figure(figsize=(9, 9))
# nx.draw(fat_tree['Graph'], pos=positions, with_labels=True, node_size=500, node_color="lightblue", edge_color="gray")
# plt.show()
