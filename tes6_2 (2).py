import numpy as np
import random
import multiprocessing as mp
from visualize import plot

pmutasi = 4
jmutasi = 2
weaknes = 10

kordinat = [[5, 80], [124, 31], [46, 54], [86, 148], [21, 8],
                   [134, 72], [49, 126], [36, 34], [26, 49], [141, 6],
                   [124, 122], [80, 92], [70, 69], [76, 133], [23, 65]]

lkota = len(kordinat)


class gen:
    kromosom = []
    fitness = 500


def fpopulasi(size):
    populasi = []
    for _ in range(size):
        genbaru = gen()
        genbaru.kromosom = random.sample(range(1, lkota), lkota - 1)
        genbaru.kromosom.insert(0, 0)
        genbaru.kromosom.append(0)
        genbaru.fitness = next(evaluasi(genbaru.kromosom))
        populasi.append(genbaru)
    yield populasi

def evaluasi(kromosom):
    lenn = lambda a, b: np.round(np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2))
    kfitness = 0
    for i in range(len(kromosom) - 1):
        p1 = kordinat[kromosom[i]]
        p2 = kordinat[kromosom[i + 1]]
        kfitness += lenn(p1, p2)
    kfitness = np.round(kfitness, 2)
    yield kfitness


def genterbaik(populasi):
    sfitness = [i.fitness for i in populasi]
    fitnessterbaik = min(sfitness)
    yield populasi[sfitness.index(fitnessterbaik)]


def TournamentSelection(populasi, k):
    selected = [populasi[np.random.randint(0, len(populasi))] for _ in range(k)]
    genfix = next(genterbaik(selected))
    yield genfix


def Reproduction(populasi):
    parent1 = next(TournamentSelection(populasi, 10)).kromosom
    parent2 = next(TournamentSelection(populasi, 6)).kromosom
    while parent1 == parent2:
        parent2 = next(TournamentSelection(populasi, 6)).kromosom

    yield next(OrderOneCrossover(parent1, parent2))


def OrderOneCrossover(parent1, parent2):
    size = len(parent1)
    child = [-1] * size

    child[0], child[size - 1] = 0, 0

    point = np.random.randint(5, size - 4)

    for i in range(point, point + 4):
        child[i] = parent1[i]

    point += 4
    point2 = point
    while child[point] in [-1, 0]:
        if child[point] != 0:
            if parent2[point2] not in child:
                child[point] = parent2[point2]
                point += 1
                if point == size: point = 0
            else:
                point2 += 1
                if point2 == size: point2 = 0
        else:
            point += 1
            if point == size:
                point = 0

    if np.random.randint(0, 3) < pmutasi:
        child = next(fmutasi(child))

    genbaru = gen()
    genbaru.kromosom = child
    genbaru.fitness = next(evaluasi(child))
    yield genbaru


def fmutasi(chromo):
    for _ in range(jmutasi):
        p1, p2 = [np.random.randint(1, len(chromo) - 1) for _ in range(2)]
        while p1 == p2:
            p2 = np.random.randint(1, len(chromo) - 1)
        log = chromo[p1]
        chromo[p1] = chromo[p2]
        chromo[p2] = log
    yield chromo


def GeneticAlgorithm(popSize, maksgenerasi):
    allBestFitness = []
    for p in fpopulasi(popSize):
        populasi = p
    generasi = 0
    while generasi < maksgenerasi:
        generasi += 1

        for _ in range(int(popSize / 2)):
            populasi.append(next(Reproduction(populasi)))

        _ = (populasi.remove(gen) if gen.fitness > weaknes else None for gen in populasi)

        averageFitness = np.round(np.sum((gen.fitness for gen in populasi)) / len(populasi), 2)
        genfix = next(genterbaik(populasi))
        print("\n")
        print(f"Generasi: {generasi}\nJumlah populasi: {len(populasi)}\nFitness Rata-rata : {averageFitness}\nFitness Terbaik: {genfix.fitness}")

        allBestFitness.append(genfix.fitness)

    # Visualize
    plot(generasi, allBestFitness, genfix, kordinat)

if __name__ == "__main__":
    p = mp.Process(target=GeneticAlgorithm, args=(100, 3))
    p.start()
    p.join()
print(lkota)
