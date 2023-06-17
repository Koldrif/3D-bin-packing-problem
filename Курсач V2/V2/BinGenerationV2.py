from BinV2 import BinV2

class BinGenerationV2:

    def __init__(self, bins: list[BinV2]):
        self.bins = bins
        self._items_count_multiplier = 10

    '''
    Return fitness of Generation
    '''
    # TODO: Add penalties
    # TODO: Maybe need make this property cached
    @property
    def cost(self):
        return \
            sum(bin_in_generation.filled_space
                   + len(bin_in_generation.items)
                for bin_in_generation in self.bins)