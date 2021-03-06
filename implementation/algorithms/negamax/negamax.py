import chess

import utils.chess_utils as evaluation

from typeguard import typechecked


@typechecked
def negamax_root(depth: int, board: chess.Board) -> (chess.Move,float):
    possible_moves  = board.legal_moves
    first_best      = -1
    best_move_final = None
    for possible_move in possible_moves:
        move = chess.Move.from_uci(str(possible_move))
        board.push(move)

        for pos in possible_moves:
            value = max(first_best, -negamax(depth - 1, board, pos))
        board.pop()

        if value > first_best:
            first_best = value
            best_move_final = move

    return best_move_final, first_best


@typechecked
def negamax(depth: int, board: chess.Board, move: chess.Move) -> float:
    if depth == 0:
        return evaluation.evaluate_board_state(board, str(move), [evaluation.TAKE_PIECES_STRATEGY])

    possible_moves = board.legal_moves
    best_move = -1

    for possible_move in possible_moves:
        move = chess.Move.from_uci(str(possible_move))
        board.push(move)

        for pos in possible_moves:
            best_move = max(best_move, -negamax(depth - 1, board, pos))

        board.pop()

        return best_move


def play() -> None:
    board = chess.Board()
    n = 0
    print(board)

    while not board.is_checkmate() and not board.is_seventyfive_moves() and not board.is_stalemate():
        if n % 2 == 0:
            move, value = negamax_root(1, board)
            print("You'are advised to do this move", move)
            move = input("Enter move:")
            move = chess.Move.from_uci(str(move))
            board.push(move)

        else:
            print("Computers Turn:")
            move, value = negamax_root(1, board)
            move = chess.Move.from_uci(str(move))
            board.push(move)

        print(board)
        n += 1


if __name__ == "__main__" :
    play()
