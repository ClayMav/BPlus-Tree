"""
This is a group project, to be worked on and completed in collaboration with
the group to which you were assigned in class.

One final report is due per group.

A number of groups, selected randomly, will be asked to demonstrate the
correctness of your program for any input data.

Your task is to develop and test a program that generates a B+ tree of order 4
for a sequence of unique index values. In addition, it must support insert and
delete operations.
1) Input is:
    a. a sequence of numeric key values (three digits at most) for initial
    generation of B+ tree, and
    b. a sequence of insert and delete commands.
2) For initial sequence of key values, your program should generate and print
out the generated index tree. In addition, for each insert and delete command
it should also generate and print out the resulting index tree.
3) Test data will be made available on April 5. Your report should show that
your program operates correctly for this test data.
4) Your final technical report should include:
    a. a description of your overall approach and the logic of your program,
    b. pseudo code for your program,
    c. output as explained in (2), and
    d. a hard copy of your program.
5) Please note that the deadline is firm and will not change under any
circumstances.
"""

import math
from graphviz import Digraph, nohtml

from node.node import Node

class BPlusTree(object):
    DEFAULT_ORDER = 3

    def __init__(self, order=DEFAULT_ORDER):
        self.order = order
        self.root = Node(order=order)

    @property
    def order(self):
        """An integer denoting the order of the tree"""
        return self._order

    @order.setter
    def order(self, value):
        """Set the order of the tree"""
        self._order = value

    @property
    def root(self):
        """The root node of the tree"""
        return self._root

    @root.setter
    def root(self, value):
        """Set the root node of the tree"""
        self._root = value

    def _insert(self, value, root=None):
        root = self.root if root is None else root

        if not root.is_leaf_node:
            split = self._insert(value, root.find_child(value))
            if split is not None:
                new_node, split_value = split
                if not root.is_split_imminent:
                    root.insert(split_value)
                    root.add_child(new_node)
                else:
                    second_new_node, second_split_value = root.insert(split_value)
                    
                    if root.find_child(new_node.max) is None:
                        root.add_child(new_node)
                    else:
                        second_new_node.add_child(new_node)
                    
                    parent_node = root.parent
                    
                    if parent_node is None:
                        parent_node = Node(values=[second_split_value], order=self.order, is_internal=True)
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
                    parent_node = Node(values=[split_value], order=self.order, is_internal=True)
                    parent_node.add_child(root)
                    parent_node.add_child(new_node)
                    self.root = parent_node
                else:
                    return new_node, split_value

    def _connect_leaves(self):
        queue = [self.root]
        leaves = []

        while queue:
            root = queue.pop(0)

            if root.is_leaf_node:
                leaves.append(root)
                if len(leaves) > 1:
                    leaves[-2].next = leaves[-1]
                    leaves[-1].prev = leaves[-2]

            for i, child in enumerate(root.children):
                if child is not None:
                    queue.append(child)

    def insert(self, value):
        self._insert(value) 
        self._connect_leaves()

    def _render_node_str(self, node):
        values = [' ']*(self.order-1)
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

            if root.next is not None:
                g.edge('%s' % (id(root),), '%s' % (id(root.next),), constraint='false')
            
            for i, child in enumerate(root.children):
                if child is not None:
                    queue.append(child)
                    g.edge('%s:f%d' % (id(root), i*2), '%s:f%d' % (id(child), self.order))

    def render(self):
        g = Digraph('g', filename='btree.gv', node_attr={'shape': 'record', 'height': '.1'})
        self._render_graph(g)
        g.view()

    def _delete(self, val, root=None):
        """Deletes specified value"""
        root = self.root if root is None else root

        if not root.is_leaf_node:
            merged = self._delete(val, root.find_child(val))

            if merged:
                if len(root.values) != root.num_children-1:
                    if root.parent:
                        return root.merge(val)
                    else:
                        if root.num_children == 1:
                            root = self.root
                            self.root = root.children[0]
                            root.remove_child(self.root)
                        else:
                            root.values.pop(-1)
        else:
            if val in root.values:
                success = root.remove(val)
                if not success:
                    if root.redistribute():
                        root.remove(val)
                    else:
                        return root.merge(val)
                        
    def delete(self, val, root=None):
        self._delete(val, root)

    def find(self, val, root=None):
        """Determines if value exists in tree"""
        # Technically this function works, but it doesn't take advantage of the
        # Optimizations of the B+ Tree. Will fix later.
        # TODO FIX
        root = self.root if root is None else root

        # Stopping Conditions
        if val in root.values:
            # If val is in this node
            return True
        if root.num_children == 0:
            # If val is not in node, and there are no children
            return False

        # Recursion
        if val <= root.values[0]:
            # If val smaller or equal to first value in the root
            # Go to first child
            print("LESS THAN OR EQUAL TO FIRST", val, root.values[0])
            return self.find(val, root.children[0])

        if val > root.values[-1]:
            # If val greater than the last value in the root
            # Go to last child
            print("GREATER THAN LAST", val, root.values[-1])
            return self.find(val, root.children[len(root.values)])

        for index, value in enumerate(root.values):
            if not index == len(root.values) - 1 and val > value and \
                    val <= root.values[index + 1]:
                # If in between two values in the root, go to child in between
                # Go to child at root.children[index + 1]
                print("BETWEEN", value, "<", val, "<=", root.values[index + 1])
                return self.find(val, root.children[index + 1])

    def __str__(self):
        return "order={}, root={}".format(self.order, self.root)
