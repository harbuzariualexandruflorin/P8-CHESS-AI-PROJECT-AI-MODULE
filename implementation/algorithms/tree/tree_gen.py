import chess
import implementation.algorithms.tree.tree as tree_node
import utils.chess_utils as evaluation
from timeit import default_timer as timer


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


def mistake_checker(move_list, player_color, mistake_threshold):
    if len(move_list) < 5:
        print("Not enough moves to check for mistakes")
        return 0

    board = chess.Board()

    if player_color == "WHITE":
        board = construct_current_state(board.copy(), move_list[:2])
        move_list.pop(0)
        move_list.pop(0)
    else:
        board = construct_current_state(board.copy(), move_list[:3])
        move_list.pop(0)
        move_list.pop(0)
        move_list.pop(0)

    while True:
        max_move_value_2 = -1
        max_move_value_1 = -1
        max_move_1 = ""
        board_copy = board.copy()

        made_move_1       = move_list[0]
        made_move_value_1 = evaluation.evaluate_board_state(board_copy.copy(), move_list[0])
        board_copy        = construct_current_state(board_copy.copy(), move_list[:1])
        made_move_value_2 = evaluation.evaluate_board_state(board_copy.copy(), move_list[1])

        board_copy = board.copy()

        for move in board_copy.legal_moves:
            current_move_value = evaluation.evaluate_board_state(board_copy.copy(), str(move))
            current_move       = str(move)

            if current_move_value > max_move_value_1:
                max_move_value_1 = current_move_value
                max_move_1       = str(current_move)

        sample_list = list()
        sample_list.append(max_move_1)
        board_copy = construct_current_state(board.copy(), sample_list)

        for move in board_copy.legal_moves:
            current_move_value = evaluation.evaluate_board_state(board_copy.copy(), str(move))

            if current_move_value > max_move_value_2:
                max_move_value_2 = current_move_value

        if made_move_value_1 <= max_move_value_1 - mistake_threshold:
            if made_move_1 != max_move_1:
                if made_move_value_2 >= max_move_value_2:
                    print("possible mistake at ", made_move_1, "\n")
                else:
                    print("questionable move at ", made_move_1, "\n")

        if len(move_list) - 2 == 0:
            break
        else:
            board = construct_current_state(board.copy(), move_list[:2])
            move_list.pop(0)
            move_list.pop(0)


if __name__ == '__main__':
    move_list = ["g1h3", "d7d6", "b2b3", "h7h6", "b3b4"]
    print(tree_gen(move_list, 2))
    print(benchmark)
    mistake_checker(move_list, "BLACK", 0)

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