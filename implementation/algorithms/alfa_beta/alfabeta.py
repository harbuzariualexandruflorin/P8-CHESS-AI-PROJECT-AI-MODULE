import chess

from utils.chess_utils import evaluate_board_state

from typeguard import typechecked

@typechecked
def alpha_beta_root(depth : int, board : chess.Board, is_maximizing : bool) -> chess.Move :
    possible_moves = board.legal_moves
    best_move = -1
    best_move_final = None
    for possible_move in possible_moves :
        move = chess.Move.from_uci(str(possible_move))
        board.push(move)
        for pos in possible_moves :
            value = max(best_move, alpha_beta(depth - 1, board, -1, 1, not is_maximizing, pos))
        board.pop()
        if value > best_move :
            best_move = value
            best_move_final = move
    return best_move_final

@typechecked
def alpha_beta(depth : int, board : chess.Board, alpha : int, beta : int, is_maximizing : bool, move : chess.Move) -> float:
    if depth == 0 :
        return -evaluate_board_state(board, str(move))
    possible_moves = board.legal_moves
    if is_maximizing :
        best_move = -1
        for possible_move in possible_moves :
            move = chess.Move.from_uci(str(possible_move))
            board.push(move)
            for pos in possible_moves :
                best_move = max(best_move, alpha_beta(depth - 1, board, alpha, beta, not is_maximizing, pos))
            board.pop()
            alpha = max(alpha, best_move)
            if beta <= alpha :
                return best_move
        return best_move
    else :
        best_move = 1
        for possible_move in possible_moves :
            move = chess.Move.from_uci(str(possible_move))
            board.push(move)
            for pos in possible_moves :
                best_move = min(best_move, alpha_beta(depth - 1, board, alpha, beta, not is_maximizing, pos))
            board.pop()
            beta = min(beta, best_move)
            if beta <= alpha :
                return best_move
        return best_move

@typechecked
def play() -> None :
    board = chess.Board()
    n = 0
    print(board)
    while not board.is_game_over() :
        if n % 2 == 0 :
            move = alpha_beta_root(1, board, True)
            print("You'are advised to do this move",move)
            move = input("Enter move:")
            move = chess.Move.from_uci(str(move))
            board.push(move)
        else:
            print("Computers Turn:")
            move = alpha_beta_root(1, board, True)
            move = chess.Move.from_uci(str(move))
            board.push(move)
        print(board)
        n += 1


if __name__ == "__main__" :
    play()