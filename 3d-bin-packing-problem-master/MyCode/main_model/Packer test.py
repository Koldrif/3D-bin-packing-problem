# from packer import *
# #
# items = [Item("Test item 1", 20, 20, 20),
#          Item('Test item 2', 10, 10,10)]
# #
# target_bins = [Bin('Test bin 1', 100, 100, 100),
#                Bin('Test bin 2', 100, 100, 100)
#                ]
#
# test = [0, 1, 2, 3, 4, 5]
# print(test[-20])


# print(f"Bin\n{target_bin}\nFilling ration: {target_bin.get_filling_ratio()}")
#
# packer = Packer()
#
# packer.add_bin(target_bin)
#
# for item in items:
#     print(f"Bin\n{target_bin}\nFilling ration: {target_bin.get_filling_ratio()}")
#
#     packer.add_item(item)
#
# print(packer.pack_to_bin(target_bin, items[0]))
# print(packer.pack_to_bin(target_bin, items[1]))
# print(packer.pack_to_bin(target_bin, items[1]))
#
# print(f"Bin\n{target_bin}\nFilling ration: {target_bin.get_filling_ratio()}")
#
#
# print(target_bin)
# parent_1 = [0, 1, 2, 3, 4, 5]
# parent_2 = [6, 7, 8, 9, 10, 11]
# print(*zip(parent_1, parent_2))
#
# crossover_counts = [(par1_arg + par2_arg) // 2 for par1_arg, par2_arg in zip(parent_1,parent_2)]
#
# print(crossover_counts)

# import GA
#
# ga = GA.GeneticAlgorithm(max_items=100, max_bins=30)
#
# ga.create_initial_population()
# ga.fill_bins_with_random_items()
#
# for bin in ga.bins:
#     print(bin.get_filling_ratio())
#     if bin.get_filling_ratio() > 1:
#
#         for item in bin.items:
#             print("\t", item)

import GA

ga = GA.GeneticAlgorithm(100, 100, 100, 2, max_items=500, max_bins=100, max_generations=100)
ga.run()

print(ga.best_scores)