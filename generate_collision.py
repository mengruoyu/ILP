# -*- coding: utf-8 -*-
from itertools import product
import numpy as np

# Generate a file collision_n.npy to store pairs (b1,c1,b2,c2) s.t. (b1,c1)~_{GIP}(b2,c2) where length of each vector is n
# To generate a file to store pairs of vector length k, replace the row "n=4" below by "n=i" and run this file.

n = 4


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

#x = 1
#print(num_to_arr(x))

def arr_to_num(arr):
    num=0
    for i in range(arr.size):
        num = num + 3**i * arr[i] 
    return int(num)

inputs = np.array(range(0, 3**n))
n_labels = 3


labels_bob = range(1, 1 + 2)
labels_carol = range(1, 1 + 4)
labels_cross = list(product(labels_bob,labels_carol))
inputs_cross = list(product(inputs,repeat = 2))
inputs_absolute = list()
for (u, v) in product(inputs, repeat=2):
    for (z, w) in product(inputs, repeat=2):
        b1 = num_to_arr(u)
        c1 = num_to_arr(v)
        b2 = num_to_arr(z)
        c2 = num_to_arr(w)
        if f(b1, c1, b2, c2):
            inputs_absolute.append((u,v,z,w))


np.save('collision_'+str(n), inputs_absolute)