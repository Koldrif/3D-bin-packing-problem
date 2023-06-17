import random

import Vector
from ItemV2 import Item, Cuboid


class BinV2(Item):

    def __init__(self, length, width, height,
                 # items: list[Item] = [],
                 pivots: list[Vector.Vector3D] = [],
                 # TODO Rotation
                 ):
        super().__init__(length, width, height)
        self.items = []
        self.pivots = pivots
        self.rotations = list()# list[str]

    def is_can_fit(self, item: Item):
        return True if self.free_space > item.volume else False

    # @staticmethod
    # def check_intersect(item1: Item, pivot1: Vector.Vector3D, item2: Item, pivot2: Vector.Vector3D) -> bool:
    #     raise NotImplementedError()
    #
    #
    # def does_item_fits(self, item: Item, pivot: Vector.Vector3D):
    #     raise NotImplementedError()

    def _is_item_fits_inside_container(self, item: Item, rotation, pivot):
        cuboid = item.to_cuboid(pivot, rotation)
        return (self.length >= cuboid.x0 >= 0 and
                self.length >= cuboid.x1 >= 0 and
                self.width >= cuboid.y0 >= 0 and
                self.width >= cuboid.y1 >= 0 and
                self.height >= cuboid.z0 >= 0 and
                self.height >= cuboid.z1 >= 0 
                )

    def try_pack(self, item: Item):
        """
        1. выбрать случайную pivot_point:
            беру 3 случайных число [0, 1)
            преобразую в координаты контейнера
        2. Методом перечисления возможных вращений смотрю, не пересекается ли мой предмет с остальными
            если да -> добавляем предмет -> сохраняем pivot_point -> сохраняем вращение
            если нет -> то скипаем
        """

        # TODO: Если предмет первый, то просто помещаем его с pivot = 0, 0, 0
        if len(self.pivots) <= 0:
            random_pivot = Vector.Vector3D(0, 0, 0)

        else:
            random_pivot = Vector.Vector3D(random.random() * self.length,
                                           random.random() * self.width,
                                           random.random() * self.height)

        for key, rotation in Vector.reflection_dictionary.items():
            """ 
            TODO Check if lies in Bin
            If YES then we check other intersections
            If NO then skip to another rotation
            """
            if not self._is_item_fits_inside_container(item, rotation, random_pivot):
                continue

            if len(self.items) == 0:
                self.items.append(item)
                self.pivots.append(random_pivot)
                self.rotations.append(key)
                continue

            for index, item_in_bin in enumerate(self.items):
                # create cuboid with pivot and vector with applied reflection
                # check if two cuboids intersect
                try:

                    placed_cuboid = Cuboid(
                        *self.pivots[index].vector,
                        *Vector.reflection_dictionary[self.rotations[index]](Vector.Vector3D(*item_in_bin.vector)).vector
                    )


                    new_cuboid = Cuboid(
                        *random_pivot.vector,
                        *rotation(Vector.Vector3D(*item.vector)).vector
                    )

                    if new_cuboid.intersects(placed_cuboid):
                        continue
                    else:
                        self.items.append(item)
                        self.pivots.append(random_pivot)
                        self.rotations.append(key)
                        return True

                except Exception as e:
                    # print("cum")
                    continue



            return False

    # Проверка, могут ли два предмета пересечься

    @property
    def filled_space(self):
        return sum([item.volume for item in self.items])

    @property
    def free_space(self):
        return self.volume - self.filled_space

    @property
    def cost(self):
        return self.filled_space + len(self.items)
