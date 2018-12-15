import chess

from typeguard import typechecked

import utils.chess_utils as chess_functions


@typechecked
def alpha_beta_root(depth: int, board: chess.Board, is_maximizing: bool, strategy : list) -> (chess.Move,float):
    possible_moves  = board.legal_moves
    best_move       = -1
    best_move_final = None
    for possible_move in possible_moves:
        move = chess.Move.from_uci(str(possible_move))
        board.push(move)
        for pos in possible_moves:
            value = max(best_move, alpha_beta(depth - 1, board, -1, 1, not is_maximizing, pos, strategy))

        board.pop()
        if value > best_move:
            best_move       = value
            best_move_final = move

    return best_move_final,best_move


@typechecked
def alpha_beta(depth: int, board: chess.Board, alpha: float, beta: float, is_maximizing: bool, move: chess.Move, strategy : list) -> float:
    if depth == 0:
        return -chess_functions.evaluate_board_state(board, str(move), strategy)

    possible_moves = board.legal_moves
    if is_maximizing:
        best_move = -1
        for possible_move in possible_moves:
            move = chess.Move.from_uci(str(possible_move))
            board.push(move)

            for pos in possible_moves:
                best_move = max(best_move, alpha_beta(depth - 1, board, alpha, beta, not is_maximizing, pos, strategy))

            board.pop()
            alpha = max(alpha, best_move)

            if beta <= alpha:
                return best_move

        return best_move
    else:
        best_move = 1

        for possible_move in possible_moves :
            move = chess.Move.from_uci(str(possible_move))
            board.push(move)

            for pos in possible_moves :
                best_move = min(best_move, alpha_beta(depth - 1, board, alpha, beta, not is_maximizing, pos, strategy))

            board.pop()
            beta = min(beta, best_move)

            if beta <= alpha:
                return best_move

        return best_move


@typechecked
def play() -> None:
    board = chess.Board()
    n     = 0

    print(board)
    while not board.is_game_over():
        if board.turn :
            move = alpha_beta_root(1, board, True, [chess_functions.DEFEND_PIECES_STRATEGY])
            print("You are advised to do this move", move)
            move = input("Enter move:")
            move = chess.Move.from_uci(str(move))
            board.push(move)
        else:
            print("Computers Turn:")
            move = alpha_beta_root(1, board, True, [chess_functions.DEFEND_PIECES_STRATEGY])
            move = chess.Move.from_uci(str(move))
            board.push(move)
        print(board)


if __name__ == "__main__" :
    play()