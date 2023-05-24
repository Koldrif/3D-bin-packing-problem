import random
from os import system, name

from models_homyakin import BackpackFactory, Item, BackpackFactoryParallelLauncher


def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def input_items(n_items):
    items = []
    for i in range(n_items):
        volume = int(input(f"Введите объем вещи {i}: "))
        cost = int(input(f"Введите стоимость вещи {i}: "))
        items.append(Item(i, volume, cost))
    return items


def run_manual(parallel=False):
    types_count = int(input("Задайте количество различных типов предметов: "))
    items = input_items(types_count)
    max_volume = int(input("Введите объем рюкзака: "))
    if parallel:
        estimator = BackpackFactoryParallelLauncher(items, max_volume)
    else:
        alpha = int(input(
            "Введите количество лучших особей из предыдущего поколения, которые будут в следующем: "))
        max_generations = int(
            input("Введите максимальное количество поколений: "))
        max_specimen = int(
            input("Введите максимальное количество особей в поколении: "))
        crossover_type = input("Введите тип кроссовера (random, avg): ")
        crossover_probability = float(
            input("Введите вероятность кроссовера: "))
        mutation_probability = float(input("Введите вероятность мутации: "))
        epsilon = float(input("Введите точность функции приспособленности: "))

        estimator = BackpackFactory(items,
                                    max_volume,
                                    alpha,
                                    max_generations,
                                    max_specimen,
                                    crossover_type,
                                    crossover_probability,
                                    mutation_probability,
                                    epsilon)
        return estimator


def run_random(parallel=False):
    types_count = int(input("Задайте количество различных типов предметов: "))
    items = [Item(i, random.randint(1, 20), random.randint(1, 20))
             for i in range(types_count)]
    max_volume = int(input("Введите объем рюкзака: "))
    if parallel:
        estimator = BackpackFactoryParallelLauncher(items, max_volume)
    else:
        estimator = BackpackFactory(items, max_volume)
    return estimator


def test_case_1(parallel=False):
    print("Объем рюкзака: 58",
          "Оптимальное решение:",
          "\t1 - 2шт, 2 - 1шт, 3 - 2шт.",
          "Запуск алгоритма:",
          sep="\n",
          end="\n")

    items = [Item(0, 7, 12),
             Item(1, 3, 2),
             Item(2, 20, 41)]
    max_volume = 58
    if parallel:
        estimator = BackpackFactoryParallelLauncher(items, max_volume)
    else:
        estimator = BackpackFactory(items, max_volume)
    return estimator


def test_case_2(parallel=False):
    print("Объем рюкзака: 45",
          "Оптимальное решение:",
          "\t1 - 0шт, 2 - 0шт, 3 - 3шт.",
          "Запуск алгоритма:",
          sep="\n",
          end="\n")

    items = [Item(0, 12, 40),
             Item(1, 20, 60),
             Item(2, 15, 50)]
    max_volume = 45
    if parallel:
        estimator = BackpackFactoryParallelLauncher(items, max_volume)
    else:
        estimator = BackpackFactory(items, max_volume)
    return estimator


def test_case_3(parallel=False):
    print("Объем рюкзака: 10",
          "Оптимальное решение:",
          "\t1 - 2шт, 2 - 0шт, 3 - 1шт, 4 - 0шт",
          "Запуск алгоритма:",
          sep="\n",
          end="\n")

    items = [Item(0, 4, 28),
             Item(1, 3, 20),
             Item(2, 2, 13),
             Item(3, 1, 6)]
    max_volume = 10
    if parallel:
        estimator = BackpackFactoryParallelLauncher(items, max_volume)
    else:
        estimator = BackpackFactory(items, max_volume)
    return estimator


def test_case_4(parallel=False):
    print("Объем рюкзака: 8",
          "Оптимальное решение:",
          "\t1 - 0шт, 2 - 1шт, 3 - 0шт, 4 - 1шт",
          "Запуск алгоритма:",
          sep="\n",
          end="\n")

    items = [Item(0, 1, 10),
             Item(1, 3, 40),
             Item(2, 4, 50),
             Item(3, 5, 70)]
    max_volume = 8
    if parallel:
        estimator = BackpackFactoryParallelLauncher(items, max_volume)
    else:
        estimator = BackpackFactory(items, max_volume)
    return estimator


def test_case_5(parallel=False):
    print("Объем рюкзака: 50",
          "Оптимальное решение (86):",
          "\t1 - 5шт, 2 - 1шт, 3 - 0шт, 4 - 0шт, 5 - 0шт, 6 - 1шт, 7 - 0шт",
          "ИЛИ",
          "\t1 - 6шт, 2 - 0шт, 3 - 0шт, 4 - 0шт, 5 - 0шт, 6 - 0шт, 7 - 1шт",
          "ИЛИ",
          "\t1 - 5шт, 2 - 0шт, 3 - 0шт, 4 - 0шт, 5 - 1шт, 6 - 2шт, 7 - 0шт",
          "ИЛИ",
          "\t1 - 4шт, 2 - 0шт, 3 - 0шт, 4 - 0шт, 5 - 0шт, 6 - 6шт, 7 - 0шт",
          "Запуск алгоритма:",
          sep="\n",
          end="\n")

    items = [Item(0, 8, 14),
             Item(1, 7, 11),
             Item(2, 6, 9),
             Item(3, 5, 7),
             Item(4, 4, 6),
             Item(5, 3, 5),
             Item(6, 2, 2)]
    max_volume = 50
    if parallel:
        estimator = BackpackFactoryParallelLauncher(items, max_volume)
    else:
        estimator = BackpackFactory(items, max_volume)
    return estimator


SWITCH = {
    "1": run_manual,
    "2": run_random,
    "3": test_case_1,
    "4": test_case_2,
    "5": test_case_3,
    "6": test_case_4,
    "7": test_case_5
}


clear()
print("Выберите способ задания начальных условий:")
print("1. Ручной")
print("2. Случайный")
print("3. Тест кейс 1")
print("4. Тест кейс 2")
print("5. Тест кейс 3")
print("6. Тест кейс 4")
print("7. Тест кейс 5")

case = input()
if case not in SWITCH:
    raise ValueError(f"Неизвестный способ задания начальных условий: {case}")

print("Выберите режим работы:")
print("1. Обычный ГА")
print("2. Параллельный ГА")

mode = input()
if mode == "1":
    mode = False
elif mode == "2":
    mode
else:
    raise ValueError(f"Неизвестный режим работы: {mode}")

choice = SWITCH[case]
estimator = choice(mode)

print("Список предметов: ")
for item in estimator.items:
    print(item)
print()

# for cost in estimator.i:
#     print(item)
# print()
import time
start = time.time()
estimator.evolve()
scores = None
if not mode:
   scores = estimator.get_info()

print("Time spend: ", time.time() - start, "seconds")

from matplotlib import pyplot as plt
plt.plot([i for i in range(1, len(scores)+1)], scores )
plt.show()
