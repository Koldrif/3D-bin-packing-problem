import functools
import random
import sys

import Vector
from ItemV2 import Item, Cuboid


class BinV2(Item):

    def __init__(self, length, width, height,
                 # items: list[Item] = [],
                 #pivots: list[Vector.Vector3D] = [],
                 max_weight: float = sys.float_info.max
                 # TODO Rotation
                 ):
        super().__init__(length, width, height, "")
        self.items = []
        self.pivots = []
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

    # def _is_item_fits_inside_container(self, item: Item, rotation, pivot):
    #     cuboid = item.to_cuboid(pivot, rotation)
    #     return (self.length >= cuboid.x0 >= 0 and
    #             self.length >= cuboid.x1 >= 0 and
    #             self.width >= cuboid.y0 >= 0 and
    #             self.width >= cuboid.y1 >= 0 and
    #             self.height >= cuboid.z0 >= 0 and
    #             self.height >= cuboid.z1 >= 0
    #             )

    def _is_item_fits_inside_container(self, cuboid: Cuboid):
        # cuboid = new_cube
        # return (self.length >= cuboid.x0 >= 0 and
        #         self.length >= cuboid.x1 >= 0 and
        #         self.width >= cuboid.y0 >= 0 and
        #         self.width >= cuboid.y1 >= 0 and
        #         self.height >= cuboid.z0 >= 0 and
        #         self.height >= cuboid.z1 >= 0
        #         )
        # return (self.length >= cuboid.x0 and cuboid.x0 >= 0 and
        #         self.length >= cuboid.x1 and cuboid.x1 >= 0 and
        #         self.width >= cuboid.y0 and cuboid.y0 >= 0 and
        #         self.width >= cuboid.y1 and cuboid.y1 >= 0 and
        #         self.height >= cuboid.z0 and cuboid.z0 >= 0 and
        #         self.height >= cuboid.z1 and cuboid.z1 >= 0
        #         )

        for i in cuboid.start + cuboid.end:
            if i < 0:
                return False

        if cuboid.y0 < 0:
            raise Exception

        return (self.length >= cuboid.x0 and cuboid.x0 >= 0 and
                self.length >= cuboid.x1 and cuboid.x1 >= 0 and
                self.width >= cuboid.y0 and cuboid.y0 >= 0 and
                self.width >= cuboid.y1 and cuboid.y1 >= 0 and
                self.height >= cuboid.z0 and cuboid.z0 >= 0 and
                self.height >= cuboid.z1 and cuboid.z1 >= 0
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
        if item.volume > self.free_space:
            return False

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

            new_cuboid = item.to_cuboid(
                random_pivot,
                rotation
            )


            # if not self._is_item_fits_inside_container(item, rotation, random_pivot):
            #     continue
            if not self._is_item_fits_inside_container(new_cuboid):
                continue


            if new_cuboid.y0 < 0:
                raise Exception

            if len(self.items) == 0:
                self.items.append(item)
                self.pivots.append(random_pivot)
                self.rotations.append(key)
                continue

            is_intersected_flag = False
            for index, item_in_bin in enumerate(self.items):
                # create cuboid with pivot and vector with applied reflection
                # check if two cuboids intersect
                if is_intersected_flag:
                    continue

                # placed_cuboid = Cuboid(
                #     *self.pivots[index].vector,
                #     *Vector.reflection_dictionary[self.rotations[index]](Vector.Vector3D(*item_in_bin.vector)).vector
                # )
                #
                placed_cuboid = item_in_bin.to_cuboid(
                    self.pivots[index],
                    Vector.reflection_dictionary[self.rotations[index]]
                )


                # new_cuboid = Cuboid(
                #     *random_pivot.vector,
                #     *rotation(Vector.Vector3D(*item.vector)).vector
                # )

                if new_cuboid.intersects(placed_cuboid):
                    is_intersected_flag = True
                    continue
                else:
                    self.items.append(item)
                    self.pivots.append(random_pivot)
                    self.rotations.append(key)

                    Cuboid.cuboids_created.append((new_cuboid.start, new_cuboid.end))
                    return True

            return False

    # Проверка, могут ли два предмета пересечься

    @property
    def filled_space(self):
        return sum([item.volume for item in self.items])

    @property
    def free_space(self):
        return self.volume - self.filled_space

    # @functools.cached_property
    @property
    def cost(self):
        return self.filled_space + len(self.items)

    def __repr__(self):
        return super().__repr__()
