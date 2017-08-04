import numpy as np
import sys

class GASort:
    def __init__(self, array, verbose=False, ascending=True, chromosomes=4):
        self.array = np.array(array)
        self.verbose = verbose
        self.ascending = ascending
        if chromosomes & 1:
            chromosomes += 1
        self.chromosomes = chromosomes

    def fitness(self, indices):
        score = 0
        for i in range(1, len(indices)):
            diff = self.array[indices[i]] - self.array[indices[i - 1]]
            if diff < 0:
                score += abs(diff)
        return score

    def generate_chromosomes(self, size=4):
        new_chromosomes = np.zeros((size, len(self.array)), dtype=int)
        for i in range(size):
            new_chromosomes[i] = np.random.permutation(len(self.array)).astype(int)
        return new_chromosomes

    def _crossover(self, c1, c2):
        j = np.random.randint(0, len(c1))

        p1 = c1
        p2 = c2
        child = np.full((len(p1)), -1)
        head = p1[j]

        run = True

        while run:
            # Copy from p1
            child[j] = p1[j]

            # Look j at p2
            jp2 = p2[j]

            if jp2 == head:
                run = False
            else:
                # Find the location of the value jp2 from p1 excluding
                # the last point so that no repitition will occur
                j = np.where(p1 == jp2)[0][0]

        for i in range(len(child)):
            if child[i] == -1:
                child[i] = p2[i]

        return child

    def crossover(self, c1, c2):
        child1 = self._crossover(c1, c2)
        child2 = self._crossover(c2, c1)
        return child1, child2

    def crossover_all(self, c):
        i = 0
        while i + 1 < len(c):
            c[i], c[i + 1] = self.crossover(c[i], c[i + 1])
            i += 2
        return c

    def mutate(self, p):
        j = np.random.randint(0, len(p), 2)
        p[j[0]], p[j[1]] = p[j[1]], p[j[0]]
        j = np.random.randint(0, len(p), 2)
        p[j[0]], p[j[1]] = p[j[1]], p[j[0]]
        return p

    def mutate_all(self, c):
        for i in range(len(c)):
            c[i] = self.mutate(c[i])
        return c

    def selection(self, chromosomes, size=0.5):
	    return chromosomes[0:int(chromosomes.shape[0] / size), :]

    def run(self, epoch=1000):
        split = 0.5
        splitted_num_of_chromosomes = int(self.chromosomes * split)

        end = False
        elite = []
        best_score = sys.maxsize
        now = 0

        chs = self.generate_chromosomes(self.chromosomes)
        while not end:
            score = np.array([int(self.fitness(i)) for i in chs])
            #print("Score: ", score)
            arr = sorted(range(len(score)), key=lambda x:score[x], reverse=False)
            #print("arridx: ", arr)
            chs[:] = chs[arr, :]
            score[:] = score[arr]

            if score[0] < best_score:
                best_score = score[0]
                elite = np.array(chs[0, :])

            chs = self.selection(chs, split)
            chs[splitted_num_of_chromosomes:,:] = self.generate_chromosomes( splitted_num_of_chromosomes)
            chs = self.crossover_all(chs)
            chs = self.mutate_all(chs)
            chs[0, :] = elite

            if now < epoch - 1:
                    print(now, best_score, end='\r\n', flush=True)
                    sys.stdout.flush()
            else:
                    print(now, best_score)
            now += 1

            if best_score == 0:
                end = True
        return elite
