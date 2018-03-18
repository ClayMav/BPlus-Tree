from node.node import Node

test_data = [42, 10, 33, 1, 5]
node = Node()


def test_node_insert():
    node.insert(test_data[0])
    assert str(node) == "{is_internal: False, depth: 4, values: [42]}"

    node.insert(test_data[1])
    assert str(node) == "{is_internal: False, depth: 4, values: [10, 42]}"

    node.insert(test_data[2])
    assert str(node) == "{is_internal: False, depth: 4, values: [10, 33, 42]}"

    node.insert(test_data[3])
    assert str(node) == "{is_internal: False, depth: 4, values: [1, 10, 33, 42]}"

    node.insert(test_data[4])
    assert str(node) == "{is_internal: False, depth: 4, values: [1, 5, 10]}"


def test_node_min():
    assert node.min, 1


def test_node_max():
    assert node.max, 10
