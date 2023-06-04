import random
from copy import deepcopy

class BackpackFactoryParallelLauncher:
    pass
class BackpackFactory:
    """
    Завод по укладыванию вещей в рюкзаки.

    :param items: Предметы
    :param max_volume: Максимальный объем рюкзака
    :param alpha: Количество лучших особей из предыдущего поколения,
        которые пойдут в следующее
    :param max_generations: Максимальное количество поколений
    :param max_specimen: Максимальное количество особей в поколении
    :param crossover_type: Тип кроссовера.
        Rand -- случайный выбор
        Avg -- среднее между родителями
    :param crossover_probability: Вероятность кроссовера
    :param mutation_probability: Вероятность мутации
    :param epsilon: Точность функции приспособленности
    """

    def __init__(self,
                 items,
                 max_volume=50,
                 alpha=2,
                 max_generations=5000,
                 max_specimen=100,
                 crossover_type="avg",
                 crossover_probability=.85,
                 mutation_probability=.1,
                 epsilon=.001):

        assert crossover_type in ("rand", "avg"), "Invalid crossover type"

        self.items = items  # List of Item
        self.types_count = len(items)
        self.max_volume = max_volume
        self.alpha = alpha
        self.max_generations = max_generations
        self.max_specimen = max_specimen
        self.crossover_type = crossover_type
        if crossover_type == "rand":
            self.crossover = self.rand_crossover
        else:
            self.crossover = self.avg_crossover
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.epsilon = epsilon

        self.cur_generation = None
        self.epochs_evolved = 0
        self.print_hyperparams()
        self.best_scores = []


    def create_rand_backpack(self):
        """Создает случайную допустимую особь."""

        backpack_volume = 0
        available_items = self.items
        item_counts = [0] * self.types_count  # изначально особь пустая
        while len(available_items) != 0:
            available_items = list(
                filter(
                    lambda x: x.volume <= self.max_volume -
                    backpack_volume,
                    available_items))
            if len(available_items) == 0:
                break
            item = random.choice(available_items)  # выбираем случайный предмет

            # выбираем случайное количество предмета
            if len(available_items) == 1:
                item_count = int(
                    (self.max_volume - backpack_volume) / item.volume)
            else:
                item_count = random.randint(
                    1, (self.max_volume - backpack_volume) // item.volume)

            # добавляем количества предмета на соответствующую позицию
            item_counts[item.number] += item_count
            # увеличиваем текущую вместимость особи
            backpack_volume += item_count * item.volume

        return Backpack(self.items, item_counts)

    def create_start_generation(self):
        """Создает стартовое поколение."""

        backpacks = [self.create_rand_backpack()
                     for _ in range(self.max_specimen)]
        return Generation(backpacks)

    def rand_crossover(self, parent_1, parent_2):
        """Проводит случайный кроссовер (случайный выбор частей родителей)."""

        for _ in range(10): 
            crossover_counts = [random.choice([par1_arg, par2_arg])
                                for par1_arg, par2_arg in zip(parent_1.item_counts,
                                                              parent_2.item_counts)]
            backpack = Backpack(self.items, crossover_counts)
            if backpack.volume <= self.max_volume:
                return backpack

        return parent_1 if parent_1.cost > parent_2.cost else parent_2

    def avg_crossover(self, parent_1, parent_2):
        """Проводит avg кроссовер (Среднее частей родителей)."""
        for _ in range(10):
            crossover_counts = [
                (par1_arg + par2_arg) // 2 for par1_arg,
                par2_arg in zip(
                    parent_1.item_counts,
                    parent_2.item_counts)]
            backpack = Backpack(self.items, crossover_counts)
            if backpack.volume <= self.max_volume:
                return backpack
        return parent_1 if parent_1.cost > parent_2.cost else parent_2

    def create_new_generation(self, generation):
        """Создает новое поколение особей."""
        new_backpacks = []

        for _ in range(2 * self.max_specimen):
            if random.random() <= self.mutation_probability:
                mutated_backpack = self.create_rand_backpack()
                new_backpacks.append(mutated_backpack)
                continue

            parent_1, parent_2 = random.sample(list(generation), k=2)

            if random.random() <= self.crossover_probability:
                crossovered_backpack = self.crossover(parent_1, parent_2)
                new_backpacks.append(crossovered_backpack)
                continue

            new_backpacks.append(
                parent_1 if parent_1.cost > parent_2.cost else parent_2)

        alpha_best = sorted(
            generation,
            key=lambda x: x.cost,
            reverse=True)[
            :self.alpha]
        new_backpacks.extend(alpha_best)
        new_backpacks = sorted(
            new_backpacks,
            key=lambda x: x.cost,
            reverse=True)

        return Generation(new_backpacks[0:self.max_specimen])

    def get_info(self):
        if self.cur_generation is None:
            return
        print(f"Прошло поколений {self.epochs_evolved}")
        print(
            f"Приспособленность текущего поколения {self.cur_generation.cost:.4f}")
        print(
            f"Лучшая особь: {sorted(self.cur_generation, key=lambda x: x.cost, reverse=True)[0]}\n")

        return self.best_scores

    def evolve(self, max_generations=None, verbose=False):
        """Запускает процесс эволюции."""

        max_generations = max_generations or self.max_generations
        if self.cur_generation is None:
            generation = self.create_start_generation()
        else:
            generation = self.cur_generation

        max_cost = generation.cost


        for i in range(1, max_generations + 1):
            self.best_scores.append(max_cost)

            self.epochs_evolved += 1
            new_generation = self.create_new_generation(generation)
            new_cost = new_generation.cost

            self.get_info()

            if i % 10 == 0:
                if verbose:
                    print(
                        f"Приспособленность поколения {i}: {generation.cost:.4f}")

            if abs(new_generation.cost - generation.cost) < self.epsilon:
                if verbose:
                    print(f"Поколение {i} -- выход")
                break

            if new_cost > max_cost:
                max_cost = new_cost

            generation = new_generation
            self.cur_generation = generation

        if verbose:
            self.get_info()
            print(f"Максимальное значение приспособленности: {max_cost:.4f}")
        return generation

    def print_hyperparams(self):
        print(f"aplha = {self.alpha}")
        print(f"max_generations = {self.max_generations}")
        print(f"max_specimen = {self.max_specimen}")
        print(f"crossover_type = {self.crossover_type}")
        print(f"crossover_probability = {self.crossover_probability:.4f}")
        print(f"mutation_probability = {self.mutation_probability:.4f}\n")


class Generation:
    """
    Поколение особей.

    :param backpacks: Список особей
    """

    def __init__(self, backpacks):
        self.backpacks = backpacks

    @property
    def cost(self):
        return sum(item.cost for item in self) / len(self)

    def append(self, item):
        self.backpacks.append(item)

    def pop(self, key):
        item = self.backpacks[key]
        del self.backpacks[key]
        return item

    def __len__(self):
        return len(self.backpacks)

    def __getitem__(self, key):
        return self.backpacks[key]

    def __delitem__(self, key):
        del self.backpacks[key]

    def __iter__(self):
        return iter(self.backpacks)

    def __repr__(self):
        objs = "\n".join(backpack.__repr__() for backpack in self)
        cost = self.cost
        return f'''Объекты: {objs}\nПриспособленность поколения: {cost}\n'''


class Backpack:
    """
    Рюкзак.

    :param items: Список всех вещей
    :param item_counts: Список из количеств каждой вещи, лежащих в рюкзаке
    """

    def __init__(self, items, item_counts):
        self.items = items
        self.item_counts = item_counts

    @property
    def cost(self):
        return sum([cnt * item.cost for cnt,
                    item in zip(self.item_counts, self.items)])

    @property
    def volume(self):
        return sum([cnt * item.volume for cnt,
                    item in zip(self.item_counts, self.items)])

    def __repr__(self):
        return "[Стоимость {}; Предметы: {}]".format(
            self.cost, self.item_counts)


class Item:
    """
    Вещь.

    :param number: Порядковый номер вещи
    :param volume: Объем вещи
    :param cost: Стоимость вещи
    """

    def __init__(self, number: int, volume: int, cost: int):
        self.number = number
        self.volume = volume
        self.cost = cost

    def __repr__(self):
        return "[Вес: {}. Стоимость: {}]".format(self.volume, self.cost)
