
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

class BPlusTree():
    DEFAULT_DEPTH = 4

    def __init__(self, depth=DEFAULT_DEPTH):
        self.depth = depth

    @property
    def depth(self)
        return self._depth

    @depth.setter
    def depth(self, value)
        self._depth = value

    def insert(self, value):
        pass
    
    def delete(self, value):
        pass

    def find(self, value):
        pass