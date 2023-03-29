# -*- coding: utf-8 -*-
from itertools import product
import numpy as np

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

# To generate a file to store pairs of vector length k, replace the row "n=4" below by "n=i" and run this file.
n = 4
inputs = np.array(range(0, 3**n))
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