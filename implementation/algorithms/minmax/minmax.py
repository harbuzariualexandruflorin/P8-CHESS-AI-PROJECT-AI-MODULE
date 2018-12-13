import chess

from typeguard import typechecked

import utils.chess_utils as chess_functions

import time

@typechecked
def min_max_root(depth : int, board : chess.Board, is_maximizing : bool, strategy : list) -> chess.Move :
    possible_moves = board.legal_moves
    best_move = -1
    second_best = -1
    third_best = -1
    best_move_final = None
    for possible_move in possible_moves :
        move = chess.Move.from_uci(str(possible_move))
        board.push(move)
        for pos in possible_moves :
            value = max(best_move, min_max(depth - 1, board, not is_maximizing, pos, strategy))
        board.pop()
        if value > best_move :
            third_best = second_best
            second_best = best_move
            best_move = value
            best_move_final = move
    return best_move_final

@typechecked
def min_max(depth : int, board : chess.Board, is_maximizing : bool, move : chess.Move, strategy : list) -> float:
    if depth == 0 :
        return -chess_functions.evaluate_board_state(board, str(move), strategy)
    possible_moves = board.legal_moves
    if is_maximizing :
        best_move = -1
        for possible_move in possible_moves :
            move = chess.Move.from_uci(str(possible_move))
            board.push(move)
            for pos in possible_moves :
                best_move = max(best_move, min_max(depth - 1, board, not is_maximizing, pos, strategy))
            board.pop()
        return best_move
    else :
        best_move = 1
        for possible_move in possible_moves :
            move = chess.Move.from_uci(str(possible_move))
            board.push(move)
            for pos in possible_moves :
                best_move = min(best_move, min_max(depth - 1, board, not is_maximizing, pos, strategy))
            board.pop()
        return best_move

@typechecked
def play() -> None :
    board = chess.Board()
    print(board)
    while not board.is_game_over() :
        if board.turn :
            start=time.time()
            move = min_max_root(2, board, True, [chess_functions.PAWN_ADVANCE_STRATEGY])
            print(chess_functions.evaluate_board_state(board, str(move), [chess_functions.PAWN_ADVANCE_STRATEGY]))
            print("You are advised to do this move",move)
            move = input("Enter move:")
            move = chess.Move.from_uci(str(move))
            board.push(move)
        else :
            start=time.time()
            print("Computer's Turn:")
            move = min_max_root(2, board, True, [chess_functions.PAWN_ADVANCE_STRATEGY])
            print(chess_functions.evaluate_board_state(board, str(move), [chess_functions.TAKE_PIECES_STRATEGY]))
            move = chess.Move.from_uci(str(move))
            board.push(move)
        print(board)
        print("Dureaza",time.time()-start)


if __name__ == "__main__" :
    play()