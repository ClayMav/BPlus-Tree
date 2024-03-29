from bplustree.bplustree import BPlusTree

test_data = [42, 12, 17, 3, 13]
tree = BPlusTree()


def test_bplustree_insert():
    tree.insert(test_data[0])
    assert str(tree) == "order=4, root={is_internal: False, order: 4, values: [42]}"

    tree.insert(test_data[1])
    assert str(tree) == "order=4, root={is_internal: False, order: 4, values: [12, 42]}"

    tree.insert(test_data[2])
    assert str(tree) == "order=4, root={is_internal: False, order: 4, values: [12, 17, 42]}"

    tree.insert(test_data[3])
    assert str(tree) == "order=4, root={is_internal: False, order: 4, values: [3, 12, 17, 42]}"

    tree.insert(test_data[4])
    assert str(tree) == "order=4, root={is_internal: True, order: 4, values: [13]}"


def test_bplustree_find():
    assert tree.find(42) is True
    assert tree.find(12) is True
    assert tree.find(17) is True
    assert tree.find(3) is True
    assert tree.find(12) is True
    assert tree.find(323) is False


def test_bplustree_delete():
    tree.delete(12)
    assert tree.find(12) is False
    tree.delete(17)
    assert tree.find(17) is False
