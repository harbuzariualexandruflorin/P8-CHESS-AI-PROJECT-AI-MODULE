import chess
import implementation.algorithms.tree.tree as tree_node
import utils.chess_utils as evaluation
from timeit import default_timer as timer
import random

benchmark = {}


def benchmarked(field):
    def outer_dec(func):
        def time_and_call(*args, **kwargs):
            start = timer()
            result = func(*args, **kwargs)
            end = timer()
            benchmark[field] = benchmark.get(field, 0) + end - start
            return result
        return time_and_call
    return outer_dec


@benchmarked("tree_gen")
def tree_gen(move_list, predicted_turns):
    max_predicted_moves = predicted_turns * 2
    board               = chess.Board()
    beginning_state     = construct_current_state(board, move_list).copy()
    root                = tree_node.TreeNode(board=beginning_state)

    for move in beginning_state.legal_moves:
        evalued_value = 0
        current_move  = chess.Move.from_uci(str(move))
        board_copy    = beginning_state.copy()
        board_copy.push(current_move)
        root.children[str(move)] = tree_node.TreeNode(parent=root, value=evalued_value, board=board_copy)
        tree_generation_recursive(1, root.children[str(move)], max_predicted_moves)

    return root


def tree_generation_recursive(current_predicted_moves, current_node, max_predicted_moves):
    if current_predicted_moves < max_predicted_moves:

        current_state = current_node.board

        for move in current_state.legal_moves:
            evalued_value = 0
            current_move  = chess.Move.from_uci(str(move))
            board_copy    = current_state.copy()
            board_copy.push(current_move)
            current_node.children[str(move)] = tree_node.TreeNode(parent=current_node, value=evalued_value, board=board_copy)
            tree_generation_recursive(current_predicted_moves + 1, current_node.children[str(move)], max_predicted_moves)


def construct_current_state(board, move_list):
    for i in range(len(move_list)):
        current_move = chess.Move.from_uci(move_list[i])
        board.push(current_move)

    return board


def mistake_checker(move_list, player, mistake_threshold):
    result_list = []
    index = 0

    if len(move_list) < 3:
        return None

    board = chess.Board()

    if player == 1:
        board = construct_current_state(board, move_list[:2])
        move_list.pop(0)
        move_list.pop(0)
        index = index+3
    else:
        board = construct_current_state(board, move_list[:3])
        move_list.pop(0)
        move_list.pop(0)
        move_list.pop(0)
        index = index+4

    while True:
        max_move_value_2 = -1
        max_move_value_1 = -1
        max_move_1 = ""
        board_copy = board.copy()
        total_gain = 0

        made_move_1       = move_list[0]
        made_move_value_1 = evaluation.evaluate_board_state(board_copy, move_list[0],[evaluation.ATTACK_PIECES_STRATEGY,evaluation.DEFEND_PIECES_STRATEGY,evaluation.KEEP_PIECES_STRATEGY])
        move = chess.Move.from_uci(str(made_move_1))
        board_copy.push(move)
        made_move_value_2 = evaluation.evaluate_board_state(board_copy, move_list[1],[evaluation.ATTACK_PIECES_STRATEGY,evaluation.DEFEND_PIECES_STRATEGY,evaluation.KEEP_PIECES_STRATEGY])

        board_copy = board.copy()
        #board_copy.pop()

        for move in board_copy.legal_moves:
            current_move_value = evaluation.evaluate_board_state(board_copy, str(move),[evaluation.ATTACK_PIECES_STRATEGY,evaluation.DEFEND_PIECES_STRATEGY,evaluation.KEEP_PIECES_STRATEGY])
            current_move       = str(move)

            if current_move_value > max_move_value_1:
                max_move_value_1 = current_move_value
                max_move_1       = str(current_move)

        total_gain = max_move_value_1-made_move_value_1
        move = chess.Move.from_uci(str(max_move_1))
        board_copy.push(move)

        for move in board_copy.legal_moves:
            current_move_value = evaluation.evaluate_board_state(board_copy, str(move),[evaluation.ATTACK_PIECES_STRATEGY,evaluation.DEFEND_PIECES_STRATEGY,evaluation.KEEP_PIECES_STRATEGY])

            if current_move_value > max_move_value_2:
                max_move_value_2 = current_move_value

        total_gain = total_gain - (made_move_value_2 - max_move_value_2)

        if made_move_value_1 <= max_move_value_1 - mistake_threshold:
            if made_move_1 != max_move_1:
                if made_move_value_2 >= max_move_value_2:
                    result_tuple = (made_move_1,index,total_gain)
                    result_list.append(result_tuple)

        if len(move_list) - 2 == 0:
            worst_mistake = find_worst_mistake(result_list)
            return worst_mistake
        else:
            board = construct_current_state(board.copy(), move_list[:2])
            move_list.pop(0)
            move_list.pop(0)
            index = index+2

def find_worst_mistake(result_list):
    worst_move = None
    worst_move_index = 0
    worst_move_gain = 100

    for i in range(0,len(result_list)):
        current_move = result_list[i][0]
        current_move_index = result_list[i][1]
        current_move_gain = result_list[i][2]
        if current_move_gain < worst_move_gain:
            worst_move = current_move
            worst_move_index = current_move_index
            worst_move_gain = current_move_gain

    return (worst_move,worst_move_index)



if __name__ == '__main__':
    #var= random.random(range(0,len(possible_moves))), "b3b4"
    move_list = ["g1h3", "d7d6", "b2b3", "h7h6", "b3b4"]
    #print(move_list[0][2:])
    print(mistake_checker(move_list, len(move_list)%2+1, 0))
    #print(tree_gen(move_list, 2))
    #print(benchmark)
    # mistake_checker(move_list, 1, 0)

    board = chess.Board()

    # for move in board.legal_moves:
    #     board_copy = board.copy()
    #     board_copy.push(move)
    #     print(board_copy)


"""

move_list=["g1h3"]
print(tree_gen(move_list, 1))



board = chess.Board()


for move in board.legal_moves:
    board_copy=board.copy()
    board_copy.push(move)
    print(board_copy)

"""