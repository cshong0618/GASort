import numpy as np
from GASort import GASort

initial = np.random.permutation(16)
#initial = np.array([2,5,87,4,32,6,-234,7453,5])
print(initial)
ga = GASort(initial, chromosomes=10)
idxs = ga.run()
print(initial)
print(idxs)
print(initial[idxs])
