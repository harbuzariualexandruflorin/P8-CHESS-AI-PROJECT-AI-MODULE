import implementation.algorithms.tree.tree as tree

from typing import *
from typeguard import typechecked

@typechecked
def alpha_beta(root: tree.TreeNode) -> str:
    alpha = -1
    beta = 1
    parent_node = alpha_beta_recursive(root, alpha, beta, True)
    parent_test = parent_node.parent
    while parent_test.parent:
        parent_node = parent_node.parent
        parent_test = parent_test.parent
    for key, value in root.children.items():
        if root.children[key] == parent_node:
            return key


@typechecked
def alpha_beta_recursive(node: tree.TreeNode, alpha: float, beta: float, maximizing_player: bool) -> tree.TreeNode:
    if not node.children:
        return node

    if maximizing_player:
        max_eval = tree.TreeNode(value=-1)
        for key, value in node.children.items():
            eval_node = alpha_beta_recursive(node.children[key], alpha, beta, False)
            eval = eval_node.value
            if max(max_eval.value, eval) != max_eval.value:
                max_eval = eval_node
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval

    else:
        min_eval = tree.TreeNode(value=1)
        for key, value in node.children.items():
            eval_node = alpha_beta_recursive(node.children[key], alpha, beta, True)
            eval = eval_node.value
            if min(min_eval.value, eval) != min_eval.value:
                min_eval = eval_node
            beta = min(beta, eval)
            if beta <= alpha:
                break
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
    root.children['move_2'].children['move_6'].children['move_13'] = tree.TreeNode(parent=root.children['move_2'].children['move_6'], value=0)
    root.children['move_2'].children['move_6'].children['move_14'] = tree.TreeNode(parent=root.children['move_2'].children['move_6'], value=0.9)


    #print(root)
    #print(root.children)
    #print(root.children['move_1'].children)
    print(alpha_beta(root))
