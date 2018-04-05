import math
from copy import deepcopy

class Node():
    DEFAULT_ORDER = 3

    def __init__(self, values=None, children=None, is_internal=False, parent=None, order=DEFAULT_ORDER):
        self._values = []
        self._children = [None]*order
        self.order = order
        self.parent = parent
        self.prev = None
        self.next = None
        self._is_internal = is_internal
        self._num_children = 0

        if values is not None:
            self.values = values
        if children is not None:
            self.children = children

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, value):
        self._next = value

    @property
    def prev(self):
        return self._prev

    @prev.setter
    def prev(self, value):
        self._prev = value

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
    def order(self):
        return self._order

    @order.setter
    def order(self, value):
        self._order = value
    
    @property
    def children(self):
        return self._children + (self._order-len(self._children))*[None]

    @children.setter
    def children(self, value):
        assert len(value) <= self._order, 'Children exceed alotted amount'
        self._children = value
        self._num_children = sum((child is not None for child in self._children))

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
        return not self.is_internal
    
    @values.setter
    def values(self, value):
        if len(value) < self.order:
            self._values = deepcopy(value)
        else:
            raise Exception('The number of values passed in should not exceed the tree order.')

    @property
    def is_split_imminent(self):
        return (len(self._values) + 1) == self.order 

    def find_insert_pos(self, value):
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
        insert_pos = self.find_insert_pos(value)
        all_values = deepcopy(self.values)
        all_values.insert(insert_pos, value)
        keep_up_to = (math.floor if self.is_internal else math.ceil)((self.order+1)/2) 
        node = Node(values=all_values[keep_up_to:], is_internal=self.is_internal, order=self.order)
        self.values = all_values[:keep_up_to-(1 if self.is_internal else 0)]

        for i, child in enumerate(self.children):
            if child is not None and child.min > all_values[keep_up_to-1]:
                for child in self.children[i:]:
                    if child is not None:
                        node.add_child(child)
                self.children = self.children[:i]
                break
                
        return node, all_values[keep_up_to-1]

    def redistribute(self):
        success = True

        if self.prev and self.prev.parent is self.parent and len(self.prev.values) >= math.ceil(self.order/2):
            idx = self.parent.children.index(self) - 1
            split_value = self.prev.values.pop(-1)
            self.insert(split_value)
            if not (self.prev.min <= self.parent.values[idx] < self.min): 
                self.parent.values[idx] = self.prev.min
        elif self.next and self.next.parent is self.parent and len(self.next.values) >= math.ceil(self.order/2):
            idx = self.parent.children.index(self.next) - 1
            split_value = self.next.values.pop(0)
            self.insert(split_value)
            if not (self.min <= self.parent.values[idx] < self.next.min): 
                self.parent.values[idx] = self.min
        else:
            success = False
        
        return success

    def merge(self, value_to_ignore):
        success = True
        left = self.prev if self.prev else self.parent.children[self.parent.children.index(self)-1]
        right = self.next 
        right_child_idx = self.parent.children.index(self)+1

        if right_child_idx < len(self.parent.children):
            right = self.parent.children[self.parent.children.index(self)+1]

        if left and left.parent is self.parent and (len(self.values) + len(left.values)) <= self.order:
            idx = self.parent.children.index(self) - 1
            for value in self.values:
                if value != value_to_ignore:
                    left.insert(value)
            if self.is_internal:
                for child in self.children:
                    if child:
                        child_idx = left.find_insert_pos(child.max)
                        found_child = left.children[child_idx]
        
                        if found_child:
                            left.values[child_idx] = found_child.max
                        
                        left.add_child(child)
        
            upper_bound = math.inf if right is None else right.min
            lower_bound = left.min
            parent = self.parent
            self.parent.remove_child(self)

            if not (lower_bound <= parent.values[idx] < upper_bound): 
                parent.values[idx] = lower_bound
        elif right and right.parent is self.parent and (len(self.values) + len(right.values)) <= self.order:
            idx = self.parent.children.index(right) - 1
            for value in self.values:
                if value != value_to_ignore:
                    right.insert(value)
            if self.is_internal:
                for child in self.children:
                    if child:
                        child_idx = right.find_insert_pos(child.max)
                        found_child = right.children[child_idx]
        
                        if found_child:
                            right.values[child_idx] = found_child.max
                        
                        right.add_child(child)
            
            upper_bound = right.min
            lower_bound = -math.inf if left is None else left.min
            parent = self.parent
            self.parent.remove_child(self)

            if not (lower_bound <= parent.values[idx] < upper_bound): 
                parent.values[idx] = lower_bound
        else:
            success = False
        
        return success
    
    def insert(self, value):
        split = None
        
        assert len(self._values) < self.order, 'Node has more than the alloted number of values.'

        if len(self._values) < self.order - 1:
            pos = self.find_insert_pos(value)
            self._values.insert(pos, value)
            self._children.insert(pos+1, None)
        else:
            split = self._split(value)
        
        return split

    def add_child(self, node):
        idx = self.find_insert_pos(node.max)
        assert idx >= len(self._children) or self.children[idx] is None, 'Cannot overwrite child node.'
        
        if idx >= len(self._children):
            self._children.append(node)
        else:
            self._children[idx] = node
        
        self.is_internal = True
        self._num_children += 1
        self.next = None
        self.prev = None
        node.parent = self

    def remove_child(self, node):
        self._children.remove(node)

        if node.prev:
            node.prev.next = node.next if node.next else None
            if node.next:
                node.next.prev = node.prev
        
        if not self._num_children:
            self.is_internal = False

        node.parent = None
        self._num_children -= 1

    def find_child(self, value):
        return self.children[self.find_insert_pos(value)]

    def remove(self, value):
        success = False

        if len(self._values) >= math.ceil(self.order/2): 
            self._values.remove(value)
            success = True
        
        return success
    

    def __str__(self):
        return '{is_internal: %s, order: %d, values: %s}' % (self.is_internal, self.order, self.values,)


if __name__ == '__main__':
    test_data = [42, 10, 33, 1, 5]
    node = Node()
    for value in test_data:
        node.insert(value)
        print(node)
    print(node.min, node.max)
