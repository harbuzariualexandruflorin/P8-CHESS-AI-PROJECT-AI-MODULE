
import chess
import implementation.algorithms.tree.tree as tree_node
import utils.chess_utils as evaluation

from typing import *
from typeguard import typechecked


#typecheck this
def tree_gen(move_list, predicted_turns):
    max_predicted_moves = predicted_turns*2
    board = chess.Board()
    beginning_state = construct_current_state(board, move_list).copy()
    root = tree_node.TreeNode()
    for move in beginning_state.legal_moves:
        evalued_value=evaluation.evaluate_board_state(beginning_state,str(move))
        root.children[str(move)] = tree_node.TreeNode(parent=root,value=evalued_value)
        tree_generation_recursive(1, root.children[str(move)], beginning_state.copy(), max_predicted_moves)
    return root


#typecheck me
def tree_generation_recursive(current_predicted_moves, current_node, beginning_state, max_predicted_moves):
    if current_predicted_moves<max_predicted_moves:
        move_list = list()
        parent = current_node
        while parent.parent:
            parent = parent.parent
            for key, values in parent.children.items():
                if parent.children[key] == current_node:
                    move_list.append(str(key))
        current_state = construct_current_state(beginning_state,move_list).copy()
        for move in current_state.generate_legal_moves():
            evalued_value = evaluation.evaluate_board_state(current_state, str(move))
            current_node.children[str(move)] = tree_node.TreeNode(parent=current_node,value=evalued_value)
            tree_generation_recursive(current_predicted_moves+1, current_node.children[str(move)], beginning_state.copy(), max_predicted_moves)


#typecheck this
def construct_current_state(board, move_list):
    i = len(move_list)
    while i > 0:
        current_move = chess.Move.from_uci(move_list[i-1])
        board.push(current_move)
        i = i-1
    return board


if __name__ == '__main__':
    move_list=["g1h3"]
    print(tree_gen(move_list, 1))


    board = chess.Board()


    for move in board.legal_moves:
        board_copy=board.copy()
        board_copy.push(move)
        print(board_copy)


