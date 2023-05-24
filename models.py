import random
import uuid
class Item:
    """
    Represents an item with various properties.

    Attributes:
        id (int): The unique identifier of the item.
        volume (float): The volume of the item.
        is_fragile (bool): Indicates whether the item is fragile or not.
        priority (int): The priority level of the item.
        incompatible_items (list): A list of items that are incompatible with this item.
    """

    def __init__(self, volume, is_fragile, priority, incompatible_items, id=uuid.uuid4().int):
        """
        Initializes a new instance of the Item class.

        Args:
            id (int): The unique identifier of the item.
            volume (float): The volume of the item.
            is_fragile (bool): Indicates whether the item is fragile or not.
            priority (int): The priority level of the item.
            incompatible_items (list): A list of items that are incompatible with this item.
        """
        self.id = id
        self.volume = volume
        self.is_fragile = is_fragile
        self.priority = priority
        self.incompatible_items = incompatible_items

    def can_be_added_to_list(self, compare_items: list):
        return not any(self.id == i.id for i in compare_items)

    def __repr__(self):
        return f'id={self.id}, volume={self.volume}, is_fragile={self.is_fragile}, priority={self.priority},' \
               f' incompatible_items={self.incompatible_items}'




# Представляет из себя индивида
class Container:
    def __init__(self, id=uuid.uuid4(), max_volume:float=255):
        self.id = id
        self.max_volume = max_volume
        self.items = []
        self.sum_of_volumes = 0

    def add_item(self, item: Item):
        if self.sum_of_volumes + item.volume < self.max_volume and item.can_be_added_to_list(self.items):
            self.items.append(item)
            self.sum_of_volumes += item.volume
            return True
        else:
            return False

    def calculate_fitness(self):
        pass

    def __repr__(self):
        return f"Container(id={self.id}, max_volume={self.max_volume}, items={self.items}, sum_of_volumes={self.sum_of_volumes})"

class Generation:
    """
        Поколение особей
        Attributes:
             containers (list[Item]): Список особей
    """
    def __init__(self, containers: list[Item]):
        self.containers = containers

    @property
    def cost(self):
        return sum(container.sum_of_volumes for container in self.containers)

    def append(self, container):
        self.containers.append(container)

    def pop(self, id: uuid.UUID.int):
        for i, container in enumerate(self.containers):
            if container.id == id:
                return self.containers.pop(i)
        return None







class GeneticAlgorithm:
    def __init__(self,
                 items: list[Item],
                 max_volume: float,
                 alpha=2,
                 max_generation=5000,
                 max_specimen = 100,
                 crossover_probability = 0.85,
                 mutation_probability = 0.1,
                 epsilon = 0.001):
        """
               Initializes a new instance of the GeneticAlgorithm class.

               Args:
                   items (list): List of items to consider in the genetic algorithm.
                   max_volume (float): Maximum volume constraint for the solution.
                   alpha (int, optional): Alpha parameter for fitness calculation. Defaults to 2.
                   max_generation (int, optional): Maximum number of generations. Defaults to 5000.
                   max_specimen (int, optional): Maximum number of specimen in each generation. Defaults to 100.
                   crossover_probability (float, optional): Probability of crossover. Defaults to 0.85.
                   mutation_probability (float, optional): Probability of mutation. Defaults to 0.1.
                   epsilon (float, optional): Small value used for floating-point comparison. Defaults to 0.001.
               """
        self.items = items
        self.max_volume:float = max_volume
        self.alpha = alpha
        self.max_generation = max_generation
        self.max_specimen = max_specimen
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.epsilon = epsilon

    def create_rand_container(self):
        available_items = [x for x in self.items if x.volume <= self.max_volume]
        container = Container(max_volume=self.max_volume)
        while available_items:
            item = random.choice(available_items)
            if not container.add_item(item):
                available_items.remove(item)
        return container



    def create_start_generation(self):
        pass

    def rand_crossover(self, parent_1, parent_2):
        pass

    def avg_crossover(self, parent_1, parent_2):
        pass

    def create_new_generation(self, generation):
        pass

    def get_info(self):
        pass

    def evolve(self, max_generations=None, verbose=False):
        pass

    def print_hyperparams(self):
        pass
