from bplustree.bplustree import BPlusTree

test_data = [42, 12, 17, 3, 12]
tree = BPlusTree()


def test_bplustree_insert():
    tree.insert(test_data[0])
    assert str(tree) == "depth=4, root={is_internal: False, depth: 4, values: [42]}"

    tree.insert(test_data[1])
    assert str(tree) == "depth=4, root={is_internal: False, depth: 4, values: [12, 42]}"

    tree.insert(test_data[2])
    assert str(tree) == "depth=4, root={is_internal: False, depth: 4, values: [12, 17, 42]}"

    tree.insert(test_data[3])
    assert str(tree) == "depth=4, root={is_internal: False, depth: 4, values: [3, 12, 17, 42]}"

    tree.insert(test_data[4])
    assert str(tree) == "depth=4, root={is_internal: True, depth: 4, values: [12]}"

def test_bplustree_find():
    assert tree.find(42) is True
    assert tree.find(12) is True
    assert tree.find(17) is True
    assert tree.find(3) is True
    assert tree.find(12) is True
    assert tree.find(323) is False
