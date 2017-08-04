import numpy as np
from GASort import GASort

initial = np.random.permutation(10)
print(initial)
ga = GASort(initial, chromosomes=10)
idxs = ga.run()
print(initial)
print(initial[idxs])
