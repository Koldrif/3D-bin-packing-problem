from GenethicAlgorithmV2 import *
import random

items = []

for _ in range(30):
    param1 = random.randint(2, 15)
    param2 = random.randint(2, 15)
    param3 = random.randint(2, 15)
    items.append(Item(param1, param2, param3))

bin = BinV2(20, 20, 20)

ga = GeneticAlgorithmV2(20, 20, 20, 3, 100, items=items, max_population_size=30)

best_bin, best_scores = ga.run()

print(best_bin)

print("Best scores\n", best_scores)
