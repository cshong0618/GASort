import numpy as np
from GASort import GASort

initial = np.random.random(10)
#initial = np.array([2,5,87,4,32,6,-234,7453,5])
print(initial)
ga = GASort(initial, chromosomes=50)
idxs = ga.run()
print(initial)
print(idxs)
print(initial[idxs])
