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


def f(y1, z1, y2, z2):
    # Check they have same Alice's vector
    if not np.array_equal((y1 + z1) % 3, (y2 + z2) % 3):
        #print("exit at 1, y1, z1, y2, z2 = " + str(y1) + ", " +str(z1) + ", " +str(y2) + ", " +str(z2))
        return False
    f1 = poly(y1, z1)
    f2 = poly(y2, z2)
    # Determine whether they have same function value
    if f1 != f2:
        #print("exit at 2, y1, z1, y2, z2 = " + str(y1) + ", " +str(z1) + ", " +str(y2) + ", " +str(z2))
        return True
    else: 
        #print("exit at 3, y1, z1, y2, z2 = " + str(y1) + ", " +str(z1) + ", " +str(y2) + ", " +str(z2))
        return False

def poly(y, z):
    a = 0
    for i in range(y.size):
        num,reminder = divmod(-1*y[i]-z[i],3)
        a = a + y[i]*z[i]*reminder 
    return a % 3

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
with open('log.txt', 'w') as f:
    sys.stdout = f
    m = build_problem(gp.Model(name = "ILP"))
#    m.print_information()
    m.optimize()
    for v in m.getVars():
        print('%s %g' % (v.VarName, v.X))


