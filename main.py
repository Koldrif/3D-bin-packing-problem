import models

item1 = models.Item(1, False, 10, [], 1)
item2 = models.Item(1, False, 10, [], 2)
item1.incompatible_items.append(item2)
print(item2.can_be_added_to_list(item1.incompatible_items))