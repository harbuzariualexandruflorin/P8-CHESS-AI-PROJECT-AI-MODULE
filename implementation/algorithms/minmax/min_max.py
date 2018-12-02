import implementation.algorithms.tree.tree as tree

from typeguard import typechecked

@typechecked
def min_max(root : tree.TreeNode ,turns_predicted : int) -> str:
    result_node = min_max_recursive(root, True)
    parent_node = result_node
    for i in range(0, turns_predicted*2-2):
        parent_node = parent_node.parent
    for key, value in root.children.items():
        if root.children[key] == parent_node:
            return key


@typechecked
def min_max_recursive(node : tree.TreeNode, maximizing_player : bool) -> tree.TreeNode:
    if not node.children:
        return node

    if maximizing_player:
        max_eval = tree.TreeNode(value=-1)
        for key, value in node.children.items():
            eval_node = min_max_recursive(node.children[key], False)
            eval = eval_node.value
            if max(max_eval.value, eval) != max_eval.value:
                max_eval = eval_node
        return max_eval

    else:
        min_eval = tree.TreeNode(value=1)
        for key, value in node.children.items():
            eval_node = min_max_recursive(node.children[key], True)
            eval = eval_node.value
            if min(min_eval.value, eval) != min_eval.value:
                min_eval = eval_node
        return min_eval



if __name__=='__main__':

    root = tree.TreeNode()
    root.children['move_1'] = tree.TreeNode(parent=root)
    root.children['move_2'] = tree.TreeNode(parent=root)
    root.children['move_1'].children['move_3'] = tree.TreeNode(parent=root.children['move_1'])
    root.children['move_1'].children['move_4'] = tree.TreeNode(parent=root.children['move_1'])
    root.children['move_2'].children['move_5'] = tree.TreeNode(parent=root.children['move_2'])
    root.children['move_2'].children['move_6'] = tree.TreeNode(parent=root.children['move_2'])
    root.children['move_1'].children['move_3'].children['move_7'] = tree.TreeNode(parent=root.children['move_1'].children['move_3'], value=-0.1)
    root.children['move_1'].children['move_3'].children['move_8'] = tree.TreeNode(parent=root.children['move_1'].children['move_3'], value=0.3)
    root.children['move_1'].children['move_4'].children['move_9'] = tree.TreeNode(parent=root.children['move_1'].children['move_4'], value=0.5)
    root.children['move_1'].children['move_4'].children['move_10'] = tree.TreeNode(parent=root.children['move_1'].children['move_4'], value=0.1)
    root.children['move_2'].children['move_5'].children['move_11'] = tree.TreeNode(parent=root.children['move_2'].children['move_5'], value=-0.6)
    root.children['move_2'].children['move_5'].children['move_12'] = tree.TreeNode(parent=root.children['move_2'].children['move_5'], value=-0.4)
    root.children['move_2'].children['move_6'].children['move_13'] = tree.TreeNode(parent=root.children['move_2'].children['move_6'], value=0.0)
    root.children['move_2'].children['move_6'].children['move_14'] = tree.TreeNode(parent=root.children['move_2'].children['move_6'], value=0.9)


    #print(root)
    #print(root.children)
    #print(root.children['move_1'].children)
    print(min_max(root,2))
