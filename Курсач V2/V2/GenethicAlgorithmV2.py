from BinV2 import *
from BinGenerationV2 import *
from enum import Enum
import time


class CrossoverType(Enum):
    single_point = 0,
    two_point = 1,
    uniform = 2,
    genome_shuffle = 3,
    head_back = 4


class GeneticAlgorithmV2:
    def __init__(
            self,

            bin_length: float,
            bin_width: float,
            bin_height: float,
            alpha: int,  # How many best bins from previous generation will be in new generation
            max_generations: int = 100,
            # max_specimen: int,
            crossover_probability: float = .85,
            mutation_probability: float = .1,
            epsilon: float = .001,
            items: list[Item] = None,
            bins: list[BinV2] = None,
            max_items: int = 100,
            max_population_size: int = 1
    ):
        self.items = items  # list['Item']
        self.max_items = max_items
        # Bins info
        self.bins = bins
        self.max_population_size = max_population_size
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
    def last_generation(self) -> BinGenerationV2:
        return self.generations[-1]

    def fill_bin(self, bin: BinV2):
        available_items = self.items.copy()

        while len(available_items) != 0:

            available_items = list(filter(
                lambda item: item.volume < bin.free_space,
                available_items
            ))

            if len(available_items) == 0:
                break

            # Get random item from available
            item = random.choice(available_items)

            res = bin.try_pack(item)
            available_items.remove(item)


    def fill_bins_with_random_items(self, bins):
        # copy from items to available items
        for bin_in_gen in bins:
            # Think I need move this to a function
            self.fill_bin(bin_in_gen)

    def create_initial_population(self):
        '''
        1. Create random items if not passed
        2. Create random bins if not passed
        :return:
        '''
        if self.items is None:
            self.items = [Item(
                               *[random.randint(1, 50) for _ in range(3)])
                          for i in range(self.max_items)]
        if self.bins is None:
            self.bins = [BinV2(
                             # *[random.randint(25, 100) for _ in range(3)])
                             self.length,
                             self.width,
                             self.height)
                         for _ in range(self.max_population_size)]
        # self.create_initial_population();
        self.fill_bins_with_random_items(self.bins)

        return BinGenerationV2(self.bins.copy())

    def crossover(self, parent_1: BinV2, parent_2: BinV2, crossover_type: CrossoverType = CrossoverType.head_back)\
            -> BinV2:
        child = BinV2(
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
                          key=lambda item: item.volume,
                          reverse=True
                          )
            back = sorted(parent_2.items[:],
                          key=lambda item: item.volume,
                          reverse=True
                          )

            while len(head) != 0 or len(back) != 0:
                if len(head) != 0:
                    # head_item = head[0]
                    # packer.pack_to_bin(child, head_item)
                    # head.remove(head_item)
                    head_item = head.pop()
                    child.try_pack(head_item)
                if len(back) != 0:
                    # back_item = back[-1]
                    # packer.pack_to_bin(child, back_item)
                    # back.remove(back_item)
                    back_item = back.pop()
                    child.try_pack(back_item)

        # Generate unique names for bins
        self.child_bins += 1
        return child

    def create_new_generation(self, generation: BinGenerationV2):
        new_bins = []
        for _ in range(2 * self.max_population_size):
            if random.random() <= self.mutation_probability:
                new_bins.append(BinV2(
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
            key=lambda bin_in_prev_gen: bin_in_prev_gen.cost,
            reverse=True)[:self.alpha]


        new_bins.extend(alpha_best)
        new_bins = sorted(new_bins,
                          key=lambda b: b.cost,
                          reverse=True)

        self.generations.append(BinGenerationV2(new_bins[:self.max_population_size]))

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

        best_bin = sorted(self.last_generation.bins,
                          key= lambda container:  sum(container.filled_space
                   + len(container.items)))
        return best_bin, self.best_scores