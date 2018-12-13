import chess
import implementation.algorithms.tree.tree as tree_node
import utils.chess_utils as evaluation

from typing import *
from typeguard import typechecked


# typecheck this
def tree_gen(move_list, predicted_turns):
    max_predicted_moves = predicted_turns * 2
    board = chess.Board()
    beginning_state = construct_current_state(board, move_list).copy()
    root = tree_node.TreeNode()

    for move in beginning_state.legal_moves:
        evalued_value = evaluation.evaluate_board_state(beginning_state, str(move))
        root.children[str(move)] = tree_node.TreeNode(parent=root, value=evalued_value)
        tree_generation_recursive(1, root.children[str(move)], beginning_state.copy(), max_predicted_moves)

    return root


# typecheck me
def tree_generation_recursive(current_predicted_moves, current_node, beginning_state, max_predicted_moves):
    if current_predicted_moves < max_predicted_moves:
        move_list = list()
        parent = current_node

        while parent.parent:
            parent = parent.parent
            for key, values in parent.children.items():
                if parent.children[key] == current_node:
                    move_list.append(str(key))

        current_state = construct_current_state(beginning_state, move_list).copy()

        for move in current_state.generate_legal_moves():
            evalued_value = evaluation.evaluate_board_state(current_state, str(move),[evaluation.PAWN_ADVANCE_STRATEGY])
            current_node.children[str(move)] = tree_node.TreeNode(parent=current_node, value=evalued_value)
            tree_generation_recursive(current_predicted_moves + 1, current_node.children[str(move)],
                                      beginning_state.copy(), max_predicted_moves)


# typecheck this
def construct_current_state(board, move_list):
    i = len(move_list)

    while i > 0:
        current_move = chess.Move.from_uci(move_list[i - 1])
        board.push(current_move)
        i = i - 1

    return board


"""

move_list=["g1h3"]
print(tree_gen(move_list, 1))



board = chess.Board()


for move in board.legal_moves:
    board_copy=board.copy()
    board_copy.push(move)
    print(board_copy)

"""


def construct_current_state1(board, move_list):
    i = 0

    while i < len(move_list):
        current_move = chess.Move.from_uci(move_list[i])
        board.push(current_move)
        i = i + 1

    return board


def mistake_checker(move_list, player_color, mistake_threshold):
    if len(move_list) < 5:
        print("Not enough moves to check for mistakes")
        return 0

    board = chess.Board()
    player = 0
    if player_color == "WHITE":
        player = 1
        board = construct_current_state1(board.copy(), move_list[:2])
        move_list.pop(0)
        move_list.pop(0)
    elif player_color == "BLACK":
        player = 2
        board = construct_current_state1(board.copy(), move_list[:3])
        move_list.pop(0)
        move_list.pop(0)
        move_list.pop(0)

    made_move_value_2 = 0
    made_move_2 = ""
    made_move_value_1 = 0
    made_move_1 = ""

    while True:
        max_move_value_2 = -1
        max_move_2 = ""
        max_move_value_1 = -1
        max_move_1 = ""
        board_copy = board.copy()

        made_move_1 = move_list[0]
        made_move_value_1 = evaluation.evaluate_board_state(board_copy.copy(), move_list[0],[evaluation.PAWN_ADVANCE_STRATEGY])
        board_copy = construct_current_state1(board_copy.copy(), move_list[:1])
        made_move_2 = move_list[1]
        made_move_value_2 = evaluation.evaluate_board_state(board_copy.copy(), move_list[1],[evaluation.PAWN_ADVANCE_STRATEGY])

        board_copy = board.copy()

        for move in board_copy.legal_moves:
            current_move_value = evaluation.evaluate_board_state(board_copy.copy(), str(move),[evaluation.PAWN_ADVANCE_STRATEGY])
            current_move = str(move)
            if current_move_value > max_move_value_1:
                max_move_value_1 = current_move_value
                max_move_1 = str(current_move)

        sample_list = list()
        sample_list.append(max_move_1)
        board_copy = construct_current_state1(board.copy(), sample_list)

        for move in board_copy.legal_moves:
            current_move_value = evaluation.evaluate_board_state(board_copy.copy(), str(move),[evaluation.PAWN_ADVANCE_STRATEGY])
            current_move = str(move)
            if current_move_value > max_move_value_2:
                max_move_value_2 = current_move_value
                max_move_2 = str(current_move)

        if made_move_value_1 <= max_move_value_1 - mistake_threshold:
            if made_move_1 != max_move_1:
                if made_move_value_2 >= max_move_value_2:
                    print("possible mistake at ", made_move_1, "\n")
                else:
                    print("questionable move at ", made_move_1, "\n")

        if len(move_list) - 2 == 0:
            break
        else:
            board = construct_current_state1(board.copy(), move_list[:2])
            move_list.pop(0)
            move_list.pop(0)


if __name__ == '__main__':
    move_list = ["g1h3", "d7d6", "b2b3", "h7h6", "b3b4"]
    # print(tree_gen(move_list, 1))
    print(mistake_checker(move_list, "BLACK", 0))

    # board = chess.Board()

    # for move in board.legal_moves:
    #    board_copy = board.copy()
    #    board_copy.push(move)
    #    print(board_copy)
