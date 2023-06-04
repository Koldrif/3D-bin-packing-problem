from packer import *
import typing
import pygad
import random
from enum import Enum
import time


class CrossoverType(Enum):
    single_point = 0,
    two_point = 1,
    uniform = 2,
    genome_shuffle = 3,
    head_back = 4


# ga = pygad.GA(
#     num_generations=num_of_generations,
#     num_genes=num_of_genes, # should get from
#
# )

class BinGeneration:
    def __init__(self, bins: list['Bin']):
        self.bins = bins
        self.cache_cost = -1

    # calculate cost of generation. Used like fitness func
    @property
    def cost(self):
        return float(sum([bin_in_generation.get_filled_volume() for bin_in_generation in self.bins]))


class GeneticAlgorithm:
    def __init__(
            self,

            bin_length: float,
            bin_width: float,
            bin_height: float,
            alpha: int,  # How many best bins from previous generation will be in new generation
            max_generations: int,
            # max_specimen: int,
            crossover_probability: float = .85,
            mutation_probability: float = .1,
            epsilon: float = .001,
            items: list['Item'] = None,
            bins: list['Bin'] = None,
            max_items: int = 100,
            max_bins: int = 1
    ):
        self.items = items  # list['Item']
        self.max_items = max_items
        # Bins info
        self.bins = bins
        self.max_bins = max_bins
        self.length = bin_length  # float
        self.width = bin_width  # float
        self.height = bin_height  # float
        # # Genetic Algorithm settings
        self.alpha = alpha  # int
        self.max_generations = max_generations  # int
        # self.max_specimen = max_specimen  # int
        # # crossover_type = "avg",
        self.crossover_probability = crossover_probability  # float
        self.mutation_probability = mutation_probability  # float
        self.epsilon = epsilon  # float

        # Additional info
        self.current_generation = None

        # Счетчик пройденных эпох
        self.epochs_evolved = 0

        # Список лучших значений в поколениях
        self.best_scores = []

        self.generations = []

        self.mutated_bins_count = 0
        self.child_bins = 0

    @property
    def last_generation(self) -> BinGeneration:
        return self.generations[-1]

    def fill_bin(self, bin: Bin):
        available_items = self.items[:]

        while len(available_items) != 0:

            available_items = list(filter(
                lambda item: item.get_volume() < bin.get_volume() - bin.get_filled_volume(),
                available_items
            ))

            if len(available_items) == 0:
                break

            # Get random item from available
            item = random.choice(available_items)

            # Check if we can pack this item
            # Yes: pack and remove from available
            # No: Jast remove

            # if we use packer, think i need to think how to use only this function
            packer = Packer()
            packer.pack_to_bin(bin, item)
            available_items.remove(item)

    def fill_bins_with_random_items(self, bins):
        # copy from items to available items
        for bin in bins:
            # Think I need move this to a function
            self.fill_bin(bin);

    def create_initial_population(self):
        '''
        1. Create random items if not passed
        2. Create random bins if not passed
        :return:
        '''
        if self.items is None:
            self.items = [Item(f"Item{i}",
                               *[random.randint(1, 50) for _ in range(3)])
                          for i in range(self.max_items)]
        if self.bins is None:
            self.bins = [Bin(f"Bin{i}",
                             # *[random.randint(25, 100) for _ in range(3)])
                             self.length,
                             self.width,
                             self.height)
                         for i in range(self.max_bins)]
        # self.create_initial_population();
        self.fill_bins_with_random_items(self.bins)

        return BinGeneration(self.bins[:])

    def crossover(self, parent_1: Bin, parent_2: Bin, crossover_type: CrossoverType = CrossoverType.head_back) -> Bin:
        child = Bin(f"Child bin{self.child_bins}",
                    self.length,
                    self.width,
                    self.height)
        if crossover_type == CrossoverType.single_point:
            raise NotImplementedError()
        elif crossover_type == CrossoverType.two_point:
            raise NotImplementedError()
        elif crossover_type == CrossoverType.genome_shuffle:
            genome_mart = parent_1.items + parent_2.items
            raise NotImplementedError()

        elif crossover_type == CrossoverType.head_back:
            head = sorted(parent_1.items,
                          key=lambda item: item.get_volume()
                          )
            back = sorted(parent_2.items[:],
                          key=lambda item: item.get_volume(),
                          reverse=True
                          )

            packer = Packer()
            while len(head) != 0 or len(back) != 0:
                if (len(head) != 0):
                    # head_item = head[0]
                    # packer.pack_to_bin(child, head_item)
                    # head.remove(head_item)
                    head_item = head.pop()
                    packer.pack_to_bin(child, head_item)
                if (len(back) != 0):
                    # back_item = back[-1]
                    # packer.pack_to_bin(child, back_item)
                    # back.remove(back_item)
                    back_item = back.pop()
                    packer.pack_to_bin(child, back_item)

        self.child_bins += 1
        return child

    def create_new_generation(self, generation: BinGeneration):
        new_bins = []
        for _ in range(2 * self.max_bins):
            if random.random() <= self.mutation_probability:
                new_bins.append(Bin(f"Mutated bin {self.mutated_bins_count}",
                                    self.length,
                                    self.width,
                                    self.height))
                self.fill_bin(new_bins[-1])
                continue

            parent_1, parent_2 = random.sample(generation.bins, k=2)

            if random.random() <= self.crossover_probability:
                crossovered_bin = self.crossover(parent_1, parent_2)
                new_bins.append(crossovered_bin)


        alpha_best = sorted(
            generation.bins,
            key=lambda bin_in_prev_gen: bin_in_prev_gen.cost(),
            reverse=True)[:self.alpha]


        new_bins.extend(alpha_best)
        new_bins = sorted(new_bins,
                          key=lambda b: b.cost(),
                          reverse=True)

        self.generations.append(BinGeneration(new_bins[:self.max_bins]))

    def run(self):
        """Starts GA"""

        if len(self.generations) == 0:
            self.generations.append(self.create_initial_population())

        max_cost = self.last_generation.cost

        for i in range(1, self.max_generations):
            start = time.time()
            # Count how many epochs was
            self.best_scores.append(max_cost)
            self.epochs_evolved += 1

            """
            here we have:
                mutation,
                crossover,
                selection
            """
            self.create_new_generation(self.last_generation)

            """
            Print some info:
                every 10 generations:
                    print Generation max_cost
            """
            # if self.epochs_evolved % 10 == 0:
            print(f"Generation {self.epochs_evolved} cost: {self.last_generation.cost}")
            print("time spend:", time.time() - start)

            # if (abs(self.last_generation.cost - self.generations[-2].cost) < self.epsilon):
            #     print(f"Generation {self.epochs_evolved} -- exit")
            #     break

            if self.last_generation.cost > max_cost:
                max_cost = self.last_generation.cost
