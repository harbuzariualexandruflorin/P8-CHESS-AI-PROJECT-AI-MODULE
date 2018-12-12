import implementation.algorithms.tree.tree as tree
import implementation.algorithms.tree.tree_gen as construction
import utils.chess_utils as evaluation


import chess

from typing import *
from typeguard import typechecked



#only takes like half a fucking minute to run

@typechecked
def alpha_beta(root: tree.TreeNode) -> str:
    alpha = -1
    beta  = 1
    move_list = list()

    parent_node = alpha_beta_recursive(root, alpha, beta, True)
    parent_test = parent_node.parent

    while True:
        for key, value in parent_test.children.items():
            if parent_test.children[key] == parent_node:
                move_list.insert(0, key)
        if parent_test.parent:
            parent_node = parent_node.parent
            parent_test = parent_test.parent
        else:
            break

    turns_to_end_game = find_end_game(move_list)

    for key, value in root.children.items():
        if root.children[key] == parent_node:
            string = str(turns_to_end_game) + " " +str(key)
            return string




def find_end_game(move_list):
    board = chess.Board()
    board = construction.construct_current_state(board, move_list)

    turns_to_endgame = 0

    while not board.is_game_over() and turns_to_endgame < 150:
        move_list.clear()
        max_gain = -1
        best_move = ""

        for move in board.legal_moves:
            current_gain = evaluation.evaluate_board_state(board, str(move))
            if max_gain <= current_gain:
                max_gain = current_gain
                best_move = str(move)

        move_list.insert(0, best_move)
        turns_to_endgame = turns_to_endgame+1
        current_move = chess.Move.from_uci(best_move)
        board.push(current_move)

    return turns_to_endgame

@typechecked
def alpha_beta_recursive(node: tree.TreeNode,
                         alpha: float,
                         beta: float,
                         maximizing_player: bool) -> tree.TreeNode:
    if not node.children:
        return node

    if maximizing_player:
        max_eval = tree.TreeNode(value=-1)

        for key, value in node.children.items():
            eval_node = alpha_beta_recursive(node.children[key], alpha, beta, False)
            eval      = eval_node.value

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
            eval      = eval_node.value

            if min(min_eval.value, eval) != min_eval.value:
                min_eval = eval_node

            beta = min(beta, eval)

            if beta <= alpha:
                break

        return min_eval




if __name__=='__main__':
    """
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
    """

    #print(root)
    #print(root.children)
    #print(root.children['move_1'].children)
    move_list = ["g1h3"]
    print(alpha_beta(construction.tree_gen(move_list, 1)))
