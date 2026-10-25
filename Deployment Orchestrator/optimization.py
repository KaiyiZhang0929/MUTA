import copy
import time
import numpy as np
import networkx as nx
from scipy.optimize import milp
from scipy.optimize import LinearConstraint
import matplotlib.pyplot as plt
import sys
from fat_tree import *


def write_array_in_A(array, value, switch, layer, X, K, option='write'):
    position = switch * len(K) + layer
    if X[position] != 'layer k:' + str(layer) + '-> s:' + str(switch):
        print('Warning! Position error in A_dict')
    if option == 'write':
        array[position] = value
    if option == 'add':
        array[position] += value

    return array


def write_array_in_A_for_new(array, value, pos, v, P, X, K, Z):
    position = len(X) + pos + v
    array[position] = value

    return array


def get_constraint(layer_dependency, P, X, Z, K, layer_required_resource, switch_resource):
    A_idx = 0
    A_dict = {}
    # ===============Dependency constraint===============
    for layer_idx in range(len(layer_dependency)):
        for path_idx in P:
            P_i = P[path_idx]
            for pi2 in range(len(P_i)):
                middle_array = np.zeros(len(X) + len(Z))
                middle_array = write_array_in_A(middle_array, 1, P_i[pi2], layer_dependency[layer_idx][1], X, K)
                for pi1 in range(pi2 + 1):
                    middle_array = write_array_in_A(middle_array, -1, P_i[pi1], layer_dependency[layer_idx][0], X, K)
                A_dict[A_idx] = {}
                A_dict[A_idx]['middle'] = copy.deepcopy(middle_array)
                A_dict[A_idx]['right']  = 0
                A_dict[A_idx]['left']   = -np.inf
                A_idx += 1

    # ===============Integrity constraint===============
    for k in range(len(K)):
        for path_idx in P:
            P_i = P[path_idx]
            middle_array = np.zeros(len(X) + len(Z))
            for s in (P_i):
                middle_array = write_array_in_A(middle_array, -1, s, k, X, K)
            A_dict[A_idx] = {}
            A_dict[A_idx]['middle'] = copy.deepcopy(middle_array)
            A_dict[A_idx]['right']  = -1
            A_dict[A_idx]['left']   = -np.inf
            A_idx += 1

    # ===============Resource constraint===============
    for p in range(2):
        used_s = []
        for p_idx in P:
            P_i = P[p_idx]
            for s in P_i:
                if s not in used_s:
                    used_s += [s]
        for s in used_s:
            middle_array = np.zeros(len(X) + len(Z))
            for k in K:
                middle_array = write_array_in_A(middle_array, layer_required_resource[p][k], s, k, X, K, option='add')
            A_dict[A_idx] = {}
            A_dict[A_idx]['middle'] = copy.deepcopy(middle_array)
            A_dict[A_idx]['right']  = switch_resource[p][s]
            A_dict[A_idx]['left']   = -np.inf
            A_idx += 1

    # ===============0-1 programming===============
    for i in range(len(X) + len(Z)):
        middle_array = np.zeros(len(X) + len(Z))
        middle_array[i] = 1
        A_dict[A_idx] = {}
        A_dict[A_idx]['middle'] = copy.deepcopy(middle_array)
        A_dict[A_idx]['right']  = 1
        A_dict[A_idx]['left']   = 0
        A_idx += 1


    # New constraints after infocom
    # equation 6 in the paper
    pos = 0
    for p_idx in P:
        P_i = P[p_idx]
        for v in range(len(P_i)):
            s = P_i[v]
            middle_array = np.zeros(len(X) + len(Z))
            middle_array = write_array_in_A(middle_array, -1, s, len(K)-1, X, K)
            middle_array = write_array_in_A_for_new(middle_array, 1, pos, v, P, X, K, Z)
            A_dict[A_idx] = {}
            A_dict[A_idx]['middle'] = copy.deepcopy(middle_array)
            A_dict[A_idx]['right']  = 0
            A_dict[A_idx]['left']   = -np.inf
            A_idx += 1
        pos += len(P_i)

    # equation 7 in the paper
    pos = 0
    for p_idx in P:
        P_i = P[p_idx]
        for v in range(len(P_i)):
            s = P_i[v]
            middle_array = np.zeros(len(X) + len(Z))
            middle_array = write_array_in_A_for_new(middle_array, 1, pos, v, P, X, K, Z)
            for u in range(v):
                middle_array = write_array_in_A(middle_array, 1, P_i[u], len(K)-1, X, K)
            A_dict[A_idx] = {}
            A_dict[A_idx]['middle'] = copy.deepcopy(middle_array)
            A_dict[A_idx]['right']  = 1
            A_dict[A_idx]['left']   = -np.inf
            A_idx += 1
        pos += len(P_i)

    # equation 8 in the paper
    pos = 0
    for p_idx in P:
        P_i = P[p_idx]
        middle_array = np.zeros(len(X) + len(Z))
        for v in range(len(P_i)):
            middle_array = write_array_in_A_for_new(middle_array, 1, pos, v, P, X, K, Z)
        A_dict[A_idx] = {}
        A_dict[A_idx]['middle'] = copy.deepcopy(middle_array)
        A_dict[A_idx]['right']  = 1
        A_dict[A_idx]['left']   = 1
        A_idx += 1
        pos += len(P_i)

    return A_dict

# Create the dependency of the layers
def generate_dependency(K):
    layer_dependency = []
    for k1 in range(len(K)):
        for k2 in range(k1 + 1, len(K)):
            layer_dependency += [[k1, k2]]

    return layer_dependency

def get_decision_variable(S, K):
    X = {}
    idx = 0
    for s in range(len(S)):
        for k in range(len(K)):
            X[idx] = 'layer k:' + str(k) + '-> s:' + str(s)
            idx += 1
    return X

def get_Z(P):
    Z = {}
    idx = 0
    for p in range(len(P)):
        for v in range(len(P[p])):
            Z[idx] = 'p:' + str(p) + '-> v:' + str(v)
            idx += 1
    return Z

def get_obj(X, Z, S, K, P):
    obj = np.zeros(len(X) + len(Z))
    # ===============Minimal memory===============
    Mem = np.ones(len(X))
    #Mem[0] += 1

    coef_obj_mem = 1
    for xi in range(len(X)):
        obj[xi] += coef_obj_mem * Mem[xi] * 33.75/2
    # ===============Minimal stage===============
    stage = np.ones(len(X))
    #stage[0] += 1

    coef_obj_stage = 1
    for xi in range(len(X)):
        obj[xi] += coef_obj_stage * stage[xi] * 33.75/2

    # For Z
    coef_obj_latency = 1
    idx = 0
    for p in range(len(P)):
        for v in range(len(P[p])):
            obj[len(X) + idx] += coef_obj_latency * (v+1)
            idx += 1

    return obj


def optimization(K, Network_Topology, layer_required_resource, switch_resource):

    P = Network_Topology['Path']
    S = Network_Topology['Device list']
    X = get_decision_variable(S, K)
    Z = get_Z(P)
    obj = get_obj(X, Z, S, K, P)
    layer_dependency = generate_dependency(K)
    constraints_dict = get_constraint(layer_dependency, P, X, Z, K, layer_required_resource, switch_resource)

    middle_ineq = np.zeros((len(constraints_dict), len(X)+len(Z)))
    right_ineq  = np.zeros(len(constraints_dict))
    left_ineq   = np.zeros(len(constraints_dict))
    for dict in constraints_dict:
        middle_ineq[dict, :] = constraints_dict[dict]['middle']
        right_ineq[dict]     = constraints_dict[dict]['right']
        left_ineq[dict]      = constraints_dict[dict]['left']

    constraints = LinearConstraint(middle_ineq, left_ineq, right_ineq)

    integrality = np.ones_like(obj)
    decision = milp(c=obj, constraints=constraints, integrality=integrality)
    if 'successful' not in decision.message:
        print(decision.message)
        print('Exit... The programmable network does not have enough resource.')

    return X, decision

start_time = time.time()

# Network setting

# n_depth = 3
# n_branch = 2
# Total_switch = 7
# in_device_list = [2,3,5,6]
# out_device_list = [0]

# n_depth = 4
# n_branch = 2
# Total_switch = 15
# in_device_list = [3,4,6,7,10,11,13,14]
# out_device_list = [0]

# n_depth = 5
# n_branch = 2
# Total_switch = 31
# in_device_list = [4,5,7,8,11,12,14,15,19,20,22,23,26,27,29,30]
# out_device_list = [0]

# n_depth = 6
# n_branch = 2
# Total_switch = 63
# in_device_list = [5,6,8,9,12,13,15,16,20,21,23,24,27,28,30,31,36,37,39,40,43,44,46,47,51,52,54,55,58,59,61,62]
# out_device_list = [0]

# n_depth = 7
# n_branch = 2
# Total_switch = 127
# in_device_list = [6,7,9,10,13,14,16,17,21,22,24,25,28,29,31,32,
#                   37,38,40,41,44,45,47,48,52,53,55,56,59,60,62,63,
#                   69,70,72,73,76,77,79,80,84,85,87,88,91,92,94,95,
#                   100,101,103,104,106,107,110,111,115,116,118,119,122,123,125,126,]
# out_device_list = [0]

#Network_Topology = generate_network_topology(n_depth, n_branch, in_device_list, out_device_list)

# in_device_list = [12, 13, 14, 15, 16, 17]
# out_device_list = [18, 19]

# in_device_list = [i for i in range(27, 42)]
# out_device_list = [42,43,44]

# in_device_list = [i for i in range(48, 76)]
# out_device_list = [76, 77, 78, 79]

in_device_list = [i for i in range(75, 120)]
out_device_list = [120,121,122,123,124]

# in_device_list = [i for i in range(48, 76)]
# out_device_list = [76, 77, 78, 79]

Network_Topology = create_fat_tree_topology(10, in_device_list, out_device_list)
Total_switch = len(Network_Topology['Device list'])

# Layer setting
L = [0,1,2]
layer_required_resource = [[16,16,16], [5, 5, 5]] # required memory and stage

switch_resource = []
memory_device = [16 for i in range(Total_switch)] # memory
stage_device = [12 for i in range(Total_switch)]  # stage
switch_resource.append(memory_device)
switch_resource.append(stage_device)

X, decision = optimization(L, Network_Topology, layer_required_resource, switch_resource)

end_time = time.time()

print(decision.message)
print(decision.x)
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")

node_codition = {}
node_codition_raw_for_test = {}
for d in range(len(Network_Topology['Device list'])):
    node_codition[d] = ' '
    node_codition_raw_for_test[d] = []

K = {0: {}, 1: {}, 2: {}}
for e in K:
    K[e]['duplication'] = 0

for x_idx in range(len(X)):
    if int(np.round(decision.x[x_idx], 1)) == 1:
        if node_codition[np.floor(x_idx / len(K))] == ' ':
            node_codition[np.floor(x_idx / len(K))] = 'K' + str(x_idx % len(K))
        else:
            node_codition[np.floor(x_idx / len(K))] += ' K' + str(x_idx % len(K))
        node_codition_raw_for_test[np.floor(x_idx / len(K))] += [x_idx % len(K)]
        K[int(x_idx % len(K))]['duplication'] += 1
for e in K:
    print('Element ', e, ' has ', K[e]['duplication'], ' duplications.')