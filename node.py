import math
from util import accepts
from copy import deepcopy

class Node():
    DEFAULT_DEPTH = 4

    def __init__(self, values=None, is_internal=False, parent=None, depth=DEFAULT_DEPTH):
        self._values = []
        self._children = [None]*(depth+1)
        self.depth = depth
        self.parent = parent
        self._is_internal = is_internal
        self._num_children = 0

        if values is not None:
            self.values = values

    @property
    def parent(self):
        return self._parent
    
    @parent.setter
    def parent(self, value):
        self._parent = value
    
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
    
    @property
    def num_children(self):
        return self._num_children

    @property
    def has_children(self):
        return self._num_children > 0

    @property
    def is_leaf_node(self):
        return not self.has_children
    
    @values.setter
    def values(self, value):
        if len(value) <= self.depth:
            self._values = deepcopy(value)
        else:
            raise Exception('The number of values passed in should not exceed the depth.')

    @property
    def is_split_imminent(self):
        return (len(self._values) + 1) > self.depth 


    def _find_insert_pos(self, value):
        idx = 0

        if len(self._values):
            for i, v in enumerate(self._values):
                lower_bound = -math.inf if not i else self._values[i-1]
                upper_bound = math.inf if i == len(self._values) else self._values[i]
                
                if lower_bound <= value <= upper_bound:
                    idx = i
                    break
            else:
                if value > self.max:
                    idx = len(self._values)
        
        return idx
    
    def _split(self, value):
        node = None
        insert_pos = self._find_insert_pos(value)
        all_values = deepcopy(self.values)
        all_values.insert(insert_pos, value)
        keep_up_to = (math.floor if self.is_internal else math.ceil)((self.depth+1)/2) 

    
        node = Node(values=all_values[keep_up_to+(1 if self.is_internal else 0):], is_internal=self.is_internal, depth=self.depth)
        self.values = all_values[:keep_up_to]
        return node, all_values[keep_up_to-1]

    def insert(self, value):
        split = None
        
        assert len(self._values) <= self.depth, 'Node has more than the alloted number of values.'

        if len(self._values) < self.depth:
            self._values.insert(self._find_insert_pos(value), value)
        else:
            split = self._split(value)
        
        return split

    def add_child(self, node):
        idx = self._find_insert_pos(node.max)
        assert self.children[idx] is None, 'Cannot overwrite child node.'
        self._children[idx] = node
        self.is_internal = True
        self._num_children += 1
        node.parent = self

    def remove_child(self, node):
        for i, child in enumerate(self._children):
            if child == node:
                self._children[i] = None
                self._num_children -= 1 
                break
        
        if not self._num_children:
            self.is_internal = False

        node.parent = None

    def find_child(self, value):
        return self._children[self._find_insert_pos(value)]

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
