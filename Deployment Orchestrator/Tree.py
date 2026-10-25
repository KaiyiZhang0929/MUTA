import copy
import numpy as np
import networkx as nx

def generate_device_list(D, n_depth, n_branch, current_depth, depth_idx, total_idx):
    if current_depth >= n_depth:
        return D, depth_idx, total_idx
    else:
        if current_depth == 0:
            D[total_idx] = [int(current_depth), int(depth_idx[current_depth])]
            total_idx += 1
            depth_idx[current_depth] += 1
            current_depth += 1
            D, depth_idx, total_idx = generate_device_list(D, n_depth, n_branch, current_depth, depth_idx, total_idx)
        else:
            for n in range(n_branch):
                D[total_idx] = [int(current_depth), int(depth_idx[current_depth])]
                total_idx += 1
                depth_idx[current_depth] += 1
                current_depth += 1
                D, depth_idx, total_idx = generate_device_list(D, n_depth, n_branch, current_depth, depth_idx, total_idx)
                current_depth -= 1

        return D, depth_idx, total_idx

def generate_adjacent_matrix(n_depth, n_branch):
    #  ================ Generate Devices connection =============
    D = {}

    depth_idx = np.zeros(n_depth)
    total_idx = 0

    D,_,_ = generate_device_list(D, n_depth, n_branch, 0, depth_idx, total_idx)

    #  ================ Generate adjacent_matrix
    adjacent_matrix = np.zeros((len(D),len(D)))

    for x in range(len(D)):
        for y in range(len(D)):
            if D[x][0] == D[y][0] - 1 and D[x][1] == np.floor(D[y][1] / n_branch):
                adjacent_matrix[x, y] = 1
            if D[x][0] == D[y][0] + 1 and D[y][1] == np.floor(D[x][1] / n_branch):
                adjacent_matrix[x, y] = 1
    return D, adjacent_matrix


def device_list_to_path(G, adjacent_matrix, in_device_list, out_device_list):
    number_devices = np.shape(adjacent_matrix)[0]
    P = {}
    path_idx = 0
    for i in in_device_list:
        for o in out_device_list:
            if i == o:
                continue
            for path in nx.all_simple_paths(G, source=i, target=o):
                P[path_idx] = path
                path_idx += 1
    return P

def generate_network_topology(n_depth, n_branch, in_device_list, out_device_list):
    Network_Topology = {}   # 'Device list', 'Adjacent Matrix', 'Graph', 'Path'

    Network_Topology['Device list'], Network_Topology['Adjacent Matrix'] = generate_adjacent_matrix(n_depth, n_branch)
    adjacent_matrix = Network_Topology['Adjacent Matrix']

    # Set the Graph from adjacent matrix
    Network_Graph = nx.DiGraph()
    for i in range(np.shape(adjacent_matrix)[0]):
        for j in range(np.shape(adjacent_matrix)[1]):
            if adjacent_matrix[i][j] == 1:
                Network_Graph.add_edge(i, j)
    Network_Topology['Graph'] = Network_Graph
    nx.draw(Network_Graph, node_size=60,font_size=8, with_labels=True)

    # Set the Path
    P = device_list_to_path(Network_Graph, adjacent_matrix, in_device_list, out_device_list)
    Network_Topology['Path'] = copy.deepcopy(P)

    return Network_Topology