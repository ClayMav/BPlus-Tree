import numpy as np
from time import sleep

from bplustree.bplustree import BPlusTree

np.random.seed(42)
data = np.random.choice(200, size=200, replace=False)

# data = [8, 5, 1, 7, 15, 24, 34, 13, 10, 11, 17, 19, 16, 2, 3, 12, 9]
tree = BPlusTree()
print('data:', data)
for value in data:
    print(value)
    tree.insert(value)
# PRERENDER
tree.render()

# WORKING
# Equal and purely to the left
# tree.delete(3)
# tree.delete(2)
# Purely to the right
# tree.delete(34)
# Middle
# tree.delete(19)
# tree.delete(10)
# tree.delete(8)
# tree.delete(11)
# tree.delete(7)

# BROKEN
# tree.delete(34)
# tree.delete(24)
# NOT CHECKING FOR EMPTY NODE
# NOT SHUFFLING OVER VALUES ON UNDERFLOW

# TESTING
tree.delete(5)

sleep(3)
tree.render()
