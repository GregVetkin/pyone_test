

def traverse_tree(tree, dotted_key):
    keys = dotted_key.split(".")
    node = tree

    for key in keys:
        if key in node:
             node = node[key]
        else:
            print("Method not founded")
            return
    

    def traverse(node, current_path):
        if isinstance(node, dict):
            for key, value in node.items():
                yield from traverse(value, current_path + [key])
        else:
            yield f"{current_path}-----{node}"

    yield from traverse(node, keys)



from _tests import TESTS


for value in traverse_tree(TESTS, 'one.system'):
    print(value)