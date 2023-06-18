from GenethicAlgorithmV2 import *
import random

# items = []

# for _ in range(30):
#     param1 = random.randint(2, 15)
#     param2 = random.randint(2, 15)
#     param3 = random.randint(2, 15)
#     items.append(Item(param1, param2, param3))

#TODO Решить проблему с тем, что у нас в crossover предметы добавляются из двух родителей, тем самым у нас берутся предметы из неоткуда
#TODO Решить преблму с упаковкой, почему-то мы можем помсщать предметы в обход коллизии и объема ящика


items = [
    Item(4, 2, 5, "Item 0"),
    Item(8, 1, 1, "Item 1"),
    Item(10, 12, 7, "Item 2"),
    Item(3, 9, 14, "Item 3"),
    Item(6, 11, 13, "Item 4"),
    Item(2, 5, 8, "Item 5"),
    Item(15, 4, 6, "Item 6"),
    Item(9, 3, 10, "Item 7"),
    Item(7, 13, 2, "Item 8"),
    Item(12, 7, 9, "Item 9"),
    Item(1, 15, 11, "Item 10"),
    Item(14, 6, 3, "Item 11"),
    Item(11, 8, 12, "Item 12"),
    Item(5, 10, 4, "Item 13"),
    Item(13, 14, 15, "Item 14"),
    Item(2, 6, 11, "Item 15"),
    Item(9, 1, 5, "Item 16"),
    Item(7, 10, 3, "Item 17"),
    Item(12, 4, 13, "Item 18"),
    Item(8, 15, 9, "Item 19"),
    Item(3, 5, 7, "Item 20"),
    Item(14, 11, 6, "Item 21"),
    Item(1, 13, 12, "Item 22"),
    Item(10, 2, 4, "Item 23"),
    Item(15, 8, 14, "Item 24"),
    Item(6, 12, 1, "Item 25"),
    Item(4, 3, 9, "Item 26"),
    Item(5, 7, 10, "Item 27"),
    Item(11, 14, 2, "Item 28"),
    Item(13, 9, 15, "Item 29")
]

bin = BinV2(10, 1, 1)
for crossover_type in [
    CrossoverType.genome_shuffle,
    # CrossoverType.head_back
    ]:
    print('Crossover type: ', crossover_type.name)
    ga = GeneticAlgorithmV2(20, 20, 20, 3, max_generations=100, items=items, max_population_size=100, crossover_type=crossover_type)

    start = time.time()
    best_bin, best_scores = ga.run()
    end = time.time()


    if len(best_bin.items) != len(best_bin.pivots) != len(best_bin.rotations):
        raise Exception

    print(best_bin)
    for index, item in enumerate(best_bin.items):
        print('********** ITEM ', item.name, ' ************')
        # cuboid = item.to_cuboid(
        #     best_bin.pivots[index],
        #
        # )
        print(f'Item size: \t\tl {item.length}, \tw {item.width}, \th {item.height}')
        print('Pivot point: \tx: {0} \ty: {1} \th: {2}'.format(*best_bin.pivots[index].vector))
        print('Start of item: \tx1 {0}, \ty1 {1}, \tz1 {2}'.format(
            *item.to_cuboid(
                best_bin.pivots[index],
                Vector.reflection_dictionary[best_bin.rotations[index]]
            ).start
        ))
        print('End of item: \tx1 {0}, \ty1 {1}, \tz1 {2}'.format(
            *item.to_cuboid(
                best_bin.pivots[index],
                Vector.reflection_dictionary[best_bin.rotations[index]]
            ).end
        ))
        print('Item rotation: ', best_bin.rotations[index])

    print("Best scores\n", best_scores)

    items_volume = 0
    for item in best_bin.items:
        items_volume += item.volume

    print('Total items volume: ', items_volume)
    print('Bin max volume: ', best_bin.volume)
    print('Time spent: ', end-start)

    # for cube_start, cube_end in Cuboid.cuboids_created:
    #     print(cube_start, cube_end)

    from matplotlib import pyplot as plt
    plt.plot([i for i in range(1, len(best_scores)+1)], best_scores )
    plt.title(crossover_type.name)
    plt.show()
