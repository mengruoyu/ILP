# -*- coding: utf-8 -*-
import gurobipy as gp
from gurobipy import GRB
from itertools import product
import numpy as np
import sys

# Calculate the ILP where 
# n is the length of each vector, lb is the number of labels used by Bob, lc is the number of labels used by Carol
# If the program returns with Solution count 0, it means the the problem is infeasible under this setting.
# Otherwise, the problem is feasible, the program will print the variables.

n = 4
lb = 4
lc = 4

# f(y1, z1, y2, z2) checks whether (y1,z1)~_{GIP}(y2,z2) is true
def f(y1, z1, y2, z2):
    # Check they have same Alice's vector
    if not np.array_equal((y1 + z1) % 3, (y2 + z2) % 3):
        return False
    f1 = poly(y1, z1)
    f2 = poly(y2, z2)
    # Determine whether they have same function value
    if f1 != f2:
        return True
    else:
        return False

# poly(y, z) calculate the GIP(x,y,z) where x = (y + z) mod 3
def poly(y, z):
    a = 0
    for i in range(y.size):
        num,reminder = divmod(-1*y[i]-z[i],3)
        a = a + y[i]*z[i]*reminder 
    return a % 3

# We store each vector as a number from 0 to 3^n - 1 where n is the length of each vector. 
# To compute the function value, we need to transform each number into an array in F_3^n
# back and forth.
# num_to_arr(num) and arr_to_num(arr) are used to perform such a transform.
def num_to_arr(num):
    a = np.array([])
    for i in range(n):
        num,reminder = divmod(num,3)
        a =np.insert(a, int(0), int(reminder))
    return np.flip(a).astype(int)
def arr_to_num(arr):
    num=0
    for i in range(arr.size):
        num = num + 3**i * arr[i] 
    return int(num)

# Read data in the "collision_n.npy" file and define other variables used to construct ILP feasibility problem later.
inputs = np.array(range(0, 3**n))
n_labels = n
labels_bob = range(1, 1 + lb)
labels_carol = range(1, 1 + lc)
labels_cross = list(product(labels_bob,labels_carol))
inputs_cross = list(product(inputs,repeat = 2))
inputs_absolute = np.load('collision_'+str(n)+'.npy')
inputs_absolute = list(map(tuple, inputs_absolute))
list_bob = [(u,l1) for u in inputs for l1 in labels_bob]
list_carol = [(v,l2) for v in inputs for l2 in labels_carol]
list_cross = [(u,v,l1,l2) for u in inputs for v in inputs for l1 in labels_bob for l2 in labels_carol]
list_absolute = [(u,v,z,w,l1,l2) for (u,v,z,w) in inputs_absolute for l1 in labels_bob for l2 in labels_carol]



# Construct the ILP feasibility problem.
def build_problem(m, **kwargs):


    # Create variables
    bob = m.addVars(inputs, labels_bob, vtype=GRB.BINARY, name="bob")
    carol = m.addVars(inputs, labels_carol, vtype=GRB.BINARY, name="carol")
    cross = m.addVars(inputs_cross, labels_cross, vtype=GRB.BINARY, name="cross")
    absolute = m.addVars(inputs_absolute, labels_cross, vtype=GRB.BINARY, name="absolute")

    m.setObjective(0, GRB.MINIMIZE)

    # --- constraints ---
    for (u, v,z, w) in inputs_absolute:
        m.addConstr(
            sum(cross[u, v, l1, l2] + cross[z, w, l1, l2]-2*absolute[u, v, z, w, l1, l2] for (l1, l2) in product(labels_bob, labels_carol))
            == 2#, "sum(model.abs[%d, %d, %d, %d, l1, l2] for (l1, l2) in product(labels_bob, labels_carol)) >= 2"  % (u,v,z,w)
        )
    
    
    for v in inputs:
        m.addConstr(
        sum(bob[v, l] for l in labels_bob) == 1, "bob's sum = 1 for %d" % v)
        m.addConstr(
        sum(carol[v, l] for l in labels_carol)  == 1, "carol's sum = 1 for %d" % v)

    # the following constraints will enforce that cross equals product of labels of bob and carol
    for (u, v) in product(inputs, repeat=2):
        for (l1, l2) in product(labels_bob, labels_carol):
            m.addConstr(cross[u, v, l1, l2] - bob[u, l1] <=0#, "cross[%d,%d,%d,%d]<=bob[%d,%d]" % (u,v,l1,l2,u,l1)
                       )
            m.addConstr(cross[u, v, l1, l2] - carol[v, l2] <= 0#, "cross[%d,%d,%d,%d]<=carol[%d,%d]" % (u,v,l1,l2,v,l2)
                       )
            m.addConstr(bob[u, l1] + carol[v, l2] - cross[u, v, l1, l2] <=  1# "cross[%d,%d,%d,%d]>=bob[%d,%d]+carol[%d,%d]-1" % (u,v,l1,l2,u,l1,v,l2)
                       )
    
    #absolute value constraints
    for (u, v,z, w) in inputs_absolute:
        for (l1, l2) in labels_cross:
            m.addConstr(
                absolute[u, v, z, w, l1, l2] <= cross[z, w, l1, l2])
            m.addConstr(
                absolute[u, v, z, w, l1, l2] <= cross[u, v, l1, l2])
            m.addConstr(
                absolute[u, v, z, w, l1, l2] >= cross[u, v, l1, l2] + cross[z, w, l1, l2] - 1)
    return m

# Run the ILP and store the result in the "log.txt" file.
# After the program is terminated, we can check the result in the following way.
# Open log.txt file and scroll down to the bottom. 
# If the ILP is infeasible, then we will see that 
# "Solution count 0"
# "Model is infeasible"
# If the ILP is feasible, then we will see that 
# "Solution count 1: 0"
# "Optimal solution found (tolerance 1.00e-04)"
with open('log.txt', 'w') as f:
    sys.stdout = f
    m = build_problem(gp.Model(name = "ILP"))
    m.optimize()


