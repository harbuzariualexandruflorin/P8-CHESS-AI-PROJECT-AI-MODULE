import chess

import  utils.chess_utils as evaluation

from typeguard import typechecked

@typechecked
def negamax_root(depth : int, board : chess.Board, strategy : list) -> (chess.Move,float) :
    best_move_final = None
    possible_moves = board.legal_moves
    first_best = -1
    second_best = -1
    third_best = -1
    for possible_move in possible_moves :
        move = chess.Move.from_uci(str(possible_move))
        board.push(move)
        for pos in possible_moves :
            value = max(first_best, -negamax(depth - 1, board, pos, strategy))
        board.pop()
        if value > first_best :
            third_best = second_best
            second_best = first_best
            first_best = value
            best_move_final = move
    return best_move_final,first_best

@typechecked
def negamax(depth : int, board : chess.Board, move : chess.Move, strategy : list) -> float:
    if depth == 0 :
        return evaluation.evaluate_board_state(board, str(move),strategy)
    possible_moves = board.legal_moves
    best_move = -1
    for possible_move in possible_moves :
        move = chess.Move.from_uci(str(possible_move))
        board.push(move)
        for pos in possible_moves :
            best_move = max(best_move, -negamax(depth - 1, board, pos))
        board.pop()
        return best_move

@typechecked
def play() -> None :
    board = chess.Board()
    n = 0
    print(board)
    while not board.is_game_over() :
        if board.turn :
            move = negamax_root(1, board, [evaluation.TAKE_PIECES_STRATEGY])
            print("You are advised to do this move",move)
            move = input("Enter move:")
            move = chess.Move.from_uci(str(move))
            board.push(move)
        else:
            print("Computers Turn:")
            move = negamax_root(1, board, [evaluation.TAKE_PIECES_STRATEGY])
            move = chess.Move.from_uci(str(move))
            board.push(move)
        print(board)


if __name__ == "__main__" :
    play()
