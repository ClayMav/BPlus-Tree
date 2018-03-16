
# This is a group project, to be worked on and completed in collaboration with the group to which you
# were assigned in class.
# One final report is due per group.
# A number of groups, selected randomly, will be asked to demonstrate the correctness of your program
# for any input data.
# Your task is to develop and test a program that generates a B+ tree of order 4 for a sequence of unique
# index values. In addition, it must support insert and delete operations.
# 1) Input is:
# a. a sequence of numeric key values (three digits at most) for initial generation of B+ tree,
# and
# b. a sequence of insert and delete commands.
# 2) For initial sequence of key values, your program should generate and print out the
# generated index tree. In addition, for each insert and delete command it should also
# generate and print out the resulting index tree.
# 3) Test data will be made available on April 5. Your report should show that your program
# operates correctly for this test data.
# 4) Your final technical report should include:
# a. a description of your overall approach and the logic of your program,
# b. pseudo code for your program,
# c. output as explained in (2), and
# d. a hard copy of your program.
# 5) Please note that the deadline is firm and will not change under any circumstances.

import numpy as np
import graphviz
from node import Node
from graphviz import Digraph, nohtml

np.random.seed(42)

class BPlusTree():
    DEFAULT_DEPTH = 4

    def __init__(self, depth=DEFAULT_DEPTH):
        self.depth = depth
        self.root = Node(depth=depth)

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, value):
        self._depth = value

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value):
        self._root = value
    
    def insert(self, value, root=None):
        root = self.root if root is None else root

        if not root.is_leaf_node:
            split = self.insert(value, root.find_child(value))
            if split is not None:
                new_node, split_value = split
                if not root.is_split_imminent:
                    root.insert(split_value)
                    root.add_child(new_node)
                else:
                    second_new_node, second_split_value = root.insert(split_value)
                    try:
                        root.add_child(new_node)
                    except:
                        second_new_node.add_child(new_node)
                    
                    parent_node = root.parent
                    
                    if parent_node is None:
                        parent_node = Node(values=[second_split_value], depth=self.depth, is_internal=True)
                        parent_node.add_child(root)
                        parent_node.add_child(second_new_node)
                        self.root = parent_node
                    else:
                        return second_new_node, second_split_value
                
        else:
            if not root.is_split_imminent:
                root.insert(value)
            else:
                new_node, split_value = root.insert(value)
                parent_node = root.parent

                if parent_node is None:
                    parent_node = Node(values=[split_value], depth=self.depth, is_internal=True)
                    parent_node.add_child(root)
                    parent_node.add_child(new_node)
                    self.root = parent_node
                else:
                    return new_node, split_value


    def _render_node_str(self, node):
        values = [' ']*self.depth
        f_idx = 0
        buffer = []

        for i, value in enumerate(node.values):
            values[i] = str(value)
        
        for i, value in enumerate(values):
            buffer.append('<f%d> |<f%d> %s|' % (f_idx, f_idx+1, value))
            f_idx += 2
        
        buffer.append('<f%d>' % (f_idx,))
        return ''.join(buffer)

    def _render_graph(self, g):
        queue = [self.root]

        while queue:
            root = queue.pop(0)
            g.node('%s' % (id(root),), nohtml(self._render_node_str(root)))

            for i, child in enumerate(root.children):
                if child is not None:
                    queue.append(child)
                    g.edge('%s:f%d' % (id(root), i*2), '%s:f%d' % (id(child), self.depth))


        
    def render(self):
        g = Digraph('g', filename='btree.gv', node_attr={'shape': 'record', 'height': '.1'})
        self._render_graph(g)
        g.view()
    
    def delete(self, value):
        pass

    def find(self, value):
        pass


if __name__ == '__main__':
    data = np.random.choice(200, size=150, replace=False)
    tree = BPlusTree()
    print('data:', data)
    for value in data:
        tree.insert(value)
    tree.render()
    

