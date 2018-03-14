import math
from util import accepts
from copy import deepcopy

class Node():
    DEFAULT_DEPTH = 4

    def __init__(self, values=None, is_internal=False, depth=DEFAULT_DEPTH):
        self._values = []
        self._children = [None]*(depth+1)
        self.depth = depth
        self._is_internal = is_internal

        if values is not None:
            self.values = values
    
    @property
    def is_internal(self):
        return self._is_internal

    @is_internal.setter
    def is_internal(self, value):
        self._is_internal = value
    
    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, value):
        self._depth = value
    
    @property
    def children(self):
        return self._children

    @property
    def min(self):
        return self._values[0]

    @property
    def max(self):
        return self._values[-1]
    
    @property
    def values(self):
        return self._values
    
    @values.setter
    def values(self, value):
        if len(value) <= self.depth:
            self._values = deepcopy(value)
        else:
            raise Exception('The number of values passed in should not exceed the depth.')

    def _find_insert_pos(self, value):
        idx = 0

        if len(self._values):
            for i, v in enumerate(self._values):
                lower_bound = -math.inf if not i else self._values[i-1]
                upper_bound = math.inf if i == len(self._values) else self._values[i]
                if lower_bound <= value <= upper_bound:
                    idx = i
                    break
        
        return idx
    
    def _split(self, value):
        node = None
        insert_pos = self._find_insert_pos(value)
        all_values = deepcopy(self.values)
        all_values.insert(insert_pos, value)
        keep_up_to = (math.floor if self.is_internal else math.ceil)((self.depth+1)/2) 

    
        node = Node(all_values[keep_up_to+(1 if self.is_internal else 0):], self.is_internal, self.depth)
        self.values = all_values[:keep_up_to]
        return node

    def insert(self, value):
        split_node = None
        
        assert len(self._values) <= self.depth, 'Node has more than the alloted number of values.'

        if len(self._values) < self.depth:
            self._values.insert(self._find_insert_pos(value), value)
        else:
            split_node = self._split(value)
        
        return split_node

    def remove(self, value):
        success = False

        if len(self._values) >= math.ceil(self.depth/2): 
            self._values.remove(value)
            success = True
        
        return success
    

    def __str__(self):
        return '{is_internal: %s, depth: %d, values: %s}' % (self.is_internal, self.depth, self.values,)


if __name__ == '__main__':
    test_data = [42, 10, 33, 1, 5]
    node = Node()
    for value in test_data:
        node.insert(value)
        print(node)
    print(node.min, node.max)
