from docplex.mp.model import Model
from fat_tree import *
from Tree import *
import time
import numpy as np

def optimization2(L, Network_Topology, layer_required_resource, switch_resource, w_C, w_L):
    mdl = Model(name="MTL_Layer_Deployment")

    S = range(len(Network_Topology['Device list']))
    P = range(len(Network_Topology['Path']) )
    K = range(len(L))
    R = range(2)

    # Resource availability and requirements
    Q = {(s, r): switch_resource[r][s] for s in S for r in R}
    O = {(k, r): layer_required_resource[r][k] for k in K for r in R}

    # Variables
    X = mdl.binary_var_matrix(K, S, name="X")  # Deployment decision variables
    Z = mdl.binary_var_matrix(P, len(Network_Topology['Path'][0]), name="Z")  # Auxiliary variables for latency

    # Dependency Constraint
    for p in P:
        path = Network_Topology['Path'][p]
        l_p = len(path)
        for e in range(0, l_p):
            for k in K[:-1]:
                if e==0:
                    mdl.add_constraint(X[k, path[0]] >= X[k + 1, path[0]], f"dependency_{p}_{e}_{k}")
                else:
                    mdl.add_constraint(mdl.sum(X[k, path[u]] for u in range(e)) >= X[k + 1, path[e]],f"dependency_{p}_{e}_{k}")

    # Integrity Constraint
    for p in P:
        path = Network_Topology['Path'][p]
        for k in K:
            mdl.add_constraint(mdl.sum(X[k, s] for s in path) >= 1,f"integrity_{p}_{k}")

    # Resource Constraints
    for s in S:
        for r in R:
            mdl.add_constraint(mdl.sum(O[k, r] * X[k, s] for k in K) <= Q[s, r],f"resource_{s}_{r}")

    # Correctness Constraints for Z
    for p in P:
        path = Network_Topology['Path'][p]
        l_p = len(path)
        for v in range(l_p):
            mdl.add_constraint(Z[p, v] <= X[len(L)-1, path[v]],f"Z_correctness_1_{p}_{v}")
            if v > 1:
                mdl.add_constraint(mdl.sum(X[len(L)-1, path[u]] for u in range(v)) + Z[p, v] <= 1,f"Z_correctness_2_{p}_{v}")
        mdl.add_constraint(mdl.sum(Z[p, v] for v in range(l_p)) == 1,f"Z_sum_{p}")

    # Objective Function
    #resource_cost = mdl.sum(O[k, r] * X[k, s] for s in S for k in K for r in R)
    resource_cost = mdl.sum(1 * X[k, s] for s in S for k in K)
    latency = mdl.sum((v+1) * Z[p, v] for p in P for v in range(len(Network_Topology['Path'][p])))
    mdl.minimize(w_C * resource_cost + w_L * latency)

    solution = mdl.solve()
    if solution:
        print("Optimal Solution Found!")

        # Dictionary to store duplications for each layer
        layer_duplications = {}
        # Count duplications for each layer
        for k in K:
            deployment_count = sum(1 for s in S if X[k, s].solution_value > 0.5)
            # Store the duplication count for this layer
            layer_duplications[k] = max(0, deployment_count)  # Count extra deployments

        # Output duplication count for each layer
        print("Duplications per layer:")
        for k, duplication in layer_duplications.items():
            print(f"Layer {k}: {duplication} duplications")

        # for k in K:
        #     for s in S:
        #         if X[k, s].solution_value > 0.5:
        #             print(f"Layer {k} deployed on Switch {s}")
    else:
        print("No feasible solution found.")
    return solution


    # optimal_solutions = []
    # objective_values = []
    # num_solutions_needed = 15
    #
    # for _ in range(num_solutions_needed):
    #     solution = mdl.solve()
    #
    #     if solution:
    #         print(f"Optimal Solution {_ + 1} Found!")
    #
    #         # Store solution
    #         current_solution = {(k, s): X[k, s].solution_value for k in K for s in S}
    #
    #         # Print solution details
    #         layer_duplications = {}
    #         for k in K:
    #             deployment_count = sum(1 for s in S if X[k, s].solution_value > 0.5)
    #             layer_duplications[k] = max(0, deployment_count)
    #
    #         print("Duplications per layer:")
    #         for k, duplication in layer_duplications.items():
    #             print(f"Layer {k}: {duplication} duplications")
    #
    #         optimal_solutions.append(current_solution)
    #
    #         # Compute and store the objective value
    #         objective_value = solution.objective_value
    #         objective_values.append(objective_value)
    #         print(f"🎯 Objective Value: {objective_value}")
    #
    #         # Add a constraint to exclude this solution in the next iteration
    #         mdl.add_constraint(
    #             mdl.sum((1 if current_solution[k, s] > 0.5 else 0) * X[k, s] for k in K for s in S)
    #             <= sum(current_solution.values()) - 1
    #         )
    #     else:
    #         print("No more feasible solutions found.")
    #         break
    #
    # return optimal_solutions

# in_device_list = [12, 13, 14, 15, 16, 17]
# out_device_list = [18, 19]

# in_device_list = [i for i in range(27, 42)]
# out_device_list = [42,43,44]

# in_device_list = [i for i in range(48, 76)]
# out_device_list = [76, 77, 78, 79]

# in_device_list = [i for i in range(75, 120)]
# out_device_list = [120,121,122,123,124]

# in_device_list = [i for i in range(108, 174)]
# out_device_list = [174, 175,176,177,178,179]

# Network_Topology = create_fat_tree_topology(12, in_device_list, out_device_list)
# Total_switch = len(Network_Topology['Device list'])

n_depth = 5
n_branch = 2
Total_switch = 31
in_device_list = [4,5,7,8,11,12,14,15,19,20,22,23,26,27,29,30]
out_device_list = [0]

Network_Topology = generate_network_topology(n_depth, n_branch, in_device_list, out_device_list)


# Layer setting
L = [0,1,2]
layer_required_resource = [[16,16,16], [5, 5, 5]] # required memory and stage

switch_resource = []
memory_device = [16 for i in range(Total_switch)] # memory
stage_device = [12 for i in range(Total_switch)]  # stage
switch_resource.append(memory_device)
switch_resource.append(stage_device)

# Weights for the objective
w_C = 33.75  # Resource consumption weight
w_L = 1.0  # Latency weight

start_time = time.time()
decision = optimization2(L, Network_Topology, layer_required_resource, switch_resource, w_C, w_L)
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
print(len(Network_Topology['Path']))
# print(decision)
# print(Network_Topology['Path'])