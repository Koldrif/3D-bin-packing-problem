import pytest
from models import Item, Container, Generation, GeneticAlgorithm
import uuid

def test_Item_can_be_added_to_list():
    # Создаем два объекта типа Item с одинаковым идентификатором
    item1 = Item(volume=1.0, is_fragile=False, priority=1, incompatible_items=[], id=1)
    item2 = Item(volume=1.0, is_fragile=False, priority=1, incompatible_items=[], id=1)
    # Проверяем, что item1 не может быть добавлен в список, содержащий item2
    assert item1.can_be_added_to_list([item2]) is False

def test_Container_add_item():
    # Создаем объект типа Item и Container
    item = Item(volume=1.0, is_fragile=False, priority=1, incompatible_items=[], id=1)
    container = Container(id=uuid.uuid4(), max_volume=10.0)
    # Проверяем, что элемент может быть добавлен в контейнер
    assert container.add_item(item) is True
    # Проверяем, что элемент действительно добавлен в контейнер
    assert len(container.items) == 1

def test_Container_add_item_exceeds_volume():
    # Создаем объект типа Item и Container с максимальным объемом 1.0
    item = Item(volume=2.0, is_fragile=False, priority=1, incompatible_items=[], id=1)
    container = Container(id=uuid.uuid4(), max_volume=1.0)
    # Проверяем, что элемент не может быть добавлен в контейнер, так как его объем превышает максимальный объем контейнера
    assert container.add_item(item) is False

def test_Generation_append():
    # Создаем объекты типа Generation и Container
    generation = Generation(containers=[])
    container = Container(id=uuid.uuid4(), max_volume=10.0)
    # Добавляем контейнер в поколение
    generation.append(container)
    # Проверяем, что контейнер был добавлен в поколение
    assert len(generation.containers) == 1

def test_Generation_pop():
    # Создаем объекты типа Generation и Container
    generation = Generation(containers=[])
    container = Container(id=uuid.uuid4(), max_volume=10.0)
    # Добавляем контейнер в поколение
    generation.append(container)
    # Удаляем контейнер из поколения
    popped_container = generation.pop(container.id)
    # Проверяем, что контейнер был удален из поколения
    assert len(generation.containers) == 0
    # Проверяем, что возвращенный контейнер имеет правильный идентификатор
    assert popped_container.id == container.id

@pytest.mark.parametrize("iteration", range(1000))  # Повторить тест 3 раза
def test_create_rand_container(iteration):
    items = [
        Item(volume=1.0, is_fragile=False, priority=1, incompatible_items=[], id=1),
        Item(volume=2.0, is_fragile=False, priority=2, incompatible_items=[], id=2),
        Item(volume=3.0, is_fragile=True, priority=3, incompatible_items=[], id=3),
        Item(volume=1.5, is_fragile=True, priority=1, incompatible_items=[], id=4),
        Item(volume=2.5, is_fragile=False, priority=2, incompatible_items=[], id=5),
        Item(volume=1.2, is_fragile=True, priority=3, incompatible_items=[], id=6),
        Item(volume=2.3, is_fragile=False, priority=1, incompatible_items=[], id=7),
        Item(volume=2.3, is_fragile=False, priority=1, incompatible_items=[], id=7),
        Item(volume=2.3, is_fragile=False, priority=1, incompatible_items=[], id=7),
        Item(volume=2.3, is_fragile=False, priority=1, incompatible_items=[], id=7),
        Item(volume=2.3, is_fragile=False, priority=1, incompatible_items=[], id=7),
        Item(volume=2.3, is_fragile=False, priority=1, incompatible_items=[], id=7),
        Item(volume=2.3, is_fragile=False, priority=1, incompatible_items=[], id=7),
        Item(volume=2.3, is_fragile=False, priority=1, incompatible_items=[], id=7),
        Item(volume=2.3, is_fragile=False, priority=1, incompatible_items=[], id=7),
        Item(volume=2.3, is_fragile=False, priority=1, incompatible_items=[], id=7),
        Item(volume=2.3, is_fragile=False, priority=1, incompatible_items=[], id=7),
        Item(volume=2.3, is_fragile=False, priority=1, incompatible_items=[], id=7),
        Item(volume=2.3, is_fragile=False, priority=1, incompatible_items=[], id=7),
        Item(volume=2.3, is_fragile=False, priority=1, incompatible_items=[], id=7),
        Item(volume=2.3, is_fragile=False, priority=1, incompatible_items=[], id=7),

    ]
    max_volume = 10.0
    ga = GeneticAlgorithm(items=items, max_volume=max_volume)

    container = ga.create_rand_container()
    print(container)

    # Проверяем, что контейнер создан
    assert isinstance(container, Container)
    # Проверяем, что суммарный объем элементов в контейнере не превышает максимальный объем
    assert container.sum_of_volumes <= max_volume
    # Проверяем, что каждый элемент в контейнере можно добавить
    for item in container.items:
        assert item.can_be_added_to_list(container.items) is False


