import numpy as np

from bplustree.bplustree import BPlusTree

data = np.random.choice(100, size=10, replace=False)
tree = BPlusTree()
print('data:', data)
for value in data:
    tree.insert(value)
tree.render()
print(tree)
